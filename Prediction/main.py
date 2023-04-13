# from dist_to_campus import dist_to_campus
# from dist_to_grocery import dist_to_grocery
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn import metrics

"""
Note:
Run `python Processing/main.py` in the root directory.
Use `pip install <package name>` to install a missing package.
"""

"""
# Load the input data from JSON file
with open('Processing/sample_addresses.json', 'r') as f:
    input_data = json.load(f)

# Extract the addresses from the input data
addresses = input_data['addresses']

# Call functions with the addresses as input
distances = dist_to_campus(addresses,False)
print(distances)
distances = dist_to_grocery(addresses,False)
print(distances)
"""

def new_section(arg_title):
    print(" ")
    print(" ")
    print("- - - - - - - - - - " + arg_title + " - - - - - - - - - -")
    print(" ")

# Create a dataframe using a JSON file
new_section("Input Loading")
with open('Processing/housing_data_processed.json') as f:
    data = json.load(f)
print("len(data):", len(data))
print("data[0]:", data[0])

# Pre-process the data:
new_section("Data Pre-processing")
# 1. Unwrap embedded dictionaries
# 2. Convert booleans to numeric values (for model training purposes)
def preprocess_dataset(arg_data):
    i_row = 0
    while i_row < len(arg_data):
        original_features = list(arg_data[i_row].keys())
        for feature in original_features:
            # Convert boolean values to numeric values:
            # * If we keep the booleans -> "TypeError: float() argument must be a string or a number"
            # * If we convert booleans to strings -> "ValueError: could not convert string to float: None"
            if feature in ['furnished', 'utilities_included', "in_unit_laundry", "gym", "parking", "female_only"]:
                if arg_data[i_row][feature] == True:
                    arg_data[i_row][feature] = 1
                elif arg_data[i_row][feature] == False:
                    arg_data[i_row][feature] = 0
                elif arg_data[i_row][feature] == None:
                    arg_data[i_row][feature] = 0

            # Expand the `distance_to_POI` field:
            if feature == "distance_to_POI":
                for poi in arg_data[i_row][feature]:
                    if poi != "bus_stop": # Ignores "bus_stop"
                        new_key = feature + ":" + poi
                        arg_data[i_row][new_key] = arg_data[i_row][feature][poi]
        i_row += 1
    # print("arg_data[2]:", arg_data[2])
    return arg_data

# Create a dataframe and drop unwanted columns:
df = pd.DataFrame(preprocess_dataset(data)).drop(columns=["address", "distance_to_POI"])

# Summary:
new_section("Dataframe Overview")
print("df.head(5):", df.head(5))
print("Shape & Dimension:", df.shape, df.ndim)
print("Info:", df.info())

# For selected columns, replace `None` values with the column average:
for column in ["rent", "num_bedrooms", "num_bathrooms", "area", "distance_to_POI:campus", "distance_to_POI:grocery"]:
    # Handle `area: 0` and `area: None`:
    if column == "area":
        df.loc[df[column] < 1, column] = None
    col_mean = round(df[column].mean())
    df[column].fillna(col_mean, inplace=True)

print("df.head(5):", df.head(5))
print("Shape & Dimension:", df.shape, df.ndim)
print("Info:", df.info())

# Price distribution:
new_section("Visualization")
plt.hist(df['rent'], bins=20, edgecolor='black')
plt.xlabel('Price')
plt.ylabel('Count')
plt.title('Price Distribution')
plt.tight_layout()
plt.show()

# Overview: Show scatter plots of all features against the price
fig = plt.figure(figsize=(20, 10))
i_plot = 1
for feature in df.columns:
    if (
        feature in ['num_bedrooms', 'num_bathrooms', 'area']
        or feature in ['furnished', 'utilities_included', "in_unit_laundry", "gym", "parking"]
        or "distance_to_POI:" in feature
    ):
        axes = fig.add_subplot(3, 4, i_plot)
        plt.scatter(df[feature], df['rent'])
        axes.set_xlabel(feature)
        axes.set_ylabel("Price")
        axes.set_title("Price vs." + feature)
        i_plot += 1
plt.show()

# Training dataset and testing dataset:
new_section("Model Training")
df_rent_dropped = df.drop("rent", axis=1)
df_train, df_test, price_train, price_test = train_test_split(df_rent_dropped, df["rent"], test_size=0.4)
print("df_train.head(5)", df_train.head(5))
print("Shape & Dimension:", df_train.shape, df_train.ndim)

# isnan() should always return false; isfinite() should always be true.
# print(np.any(np.isnan(df_train)), np.any(np.isfinite(df_train)), np.any(np.isnan(price_train)), np.any(np.isfinite(price_train)))

def get_lin_reg_model(arg_model_type, arg_alpha=None):
    lin_reg_obj = None
    if arg_model_type == "Standard":
        lin_reg_obj = LinearRegression()
    elif arg_model_type == "Lasso":
        if arg_alpha == None:
            raise Exception("Lasso(): Please specify the Alpha value!")
        lin_reg_obj = Lasso(arg_alpha)
    elif arg_model_type == "Ridge":
        if arg_alpha == None:
            raise Exception("Ridge(): Please specify the Alpha value!")
        lin_reg_obj = Ridge(arg_alpha)
    return lin_reg_obj

# Train the model using different alpha values:
for alpha_ridge in [0, 0.1, 1, 3, 10, 20, 50, 100, 1000]:
    lin_reg_obj = get_lin_reg_model("Ridge", alpha_ridge)
    lin_reg_obj.fit(df_train, price_train)
    correlations = pd.DataFrame(lin_reg_obj.coef_, df_rent_dropped.columns, columns = ['Coeff'])
    print("Correlations:", correlations)

    # Test the model:
    new_section("Evaluating Model Accuracy")
    predictions = lin_reg_obj.predict(df_test)
    plt.clf() # Clears the figrue
    plt.scatter(price_test, predictions)
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.plot(np.linspace(0,5,100), np.linspace(0,5,100), '-r')
    # plt.show()
    plt.savefig('actual_vs_predicted-alpha=' + str(alpha_ridge) + '.png')

    # Visualize the residuals:
    plt.clf() # Clears the figrue
    plt.hist(price_test - predictions, edgecolor='black')
    plt.ylabel("Count")
    plt.xlabel("Residual")
    # plt.show()
    plt.savefig('residuals-alpha=' + str(alpha_ridge) + '.png')

    # TCUITODO: Issue: The saved "residual plots" are actually scattered plots.

    print(
        "Alpha: " + str(alpha_ridge),
        "Mean absolute & squared error:",
        metrics.mean_absolute_error(price_test, predictions),
        metrics.mean_squared_error(price_test, predictions)
    )
    # np.sqrt(metrics.mean_squared_error(price_test, predictions))



