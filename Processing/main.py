# from dist_to_campus import dist_to_campus
# from dist_to_grocery import dist_to_grocery
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

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

# Create a dataframe using a JSON file
with open('Processing/sample_dataset.json') as f:
    data = json.load(f)
print("len(data):", len(data))
print("data[0]:", data[0])

# Pre-process the data:
# 1. Unwrap embedded dictionaries
# 2. Convert booleans to numeric values (for model training purposes)
def preprocess_dataset(arg_data):
    i_row = 0
    while i_row < len(arg_data):
        features = list(arg_data[i_row].keys())
        for feature in features:
            if arg_data[i_row][feature] == None:
                arg_data[i_row][feature] = -1
                if feature == "rent":
                    arg_data[i_row][feature] = 0
            if feature in ['furnished', 'utilities_included', "in_unit_laundry", "gym", "parking", "female_only"]:
                if arg_data[i_row][feature] == True:
                    arg_data[i_row][feature] = 1
                elif arg_data[i_row][feature] == False:
                    arg_data[i_row][feature] = 0
                else: # TCUITODO: Handle `utilities_included` being a dictionary
                    arg_data[i_row][feature] = -1
            if feature == "distance_to_POI":
                for poi in arg_data[i_row][feature]:
                    if poi != "bus_stop": # TCUITODO: Handle "bus_stop"
                        new_key = feature + ":" + poi
                        arg_data[i_row][new_key] = arg_data[i_row][feature][poi]
        i_row += 1
    print("arg_data[2]:", arg_data[2])
    return arg_data

# Create a dataframe and drop unwanted columns:
df = pd.DataFrame(preprocess_dataset(data)).drop(columns=["address", "distance_to_POI"])

# Summary:
print(df.head(5))
print(df.shape, df.ndim)
print(df.info())

# Price distribution:
# prices = df['rent'][~np.isnan(df['rent'])] # filters out `nan` values
plt.hist(df['rent'], bins=20, edgecolor='black')
plt.xlabel('Price')
plt.ylabel('Count')
plt.title('Price Distribution')
plt.tight_layout()
# plt.show() # TCUITODO: Re-enable this

# Overview: Show scatter plots of all features against the price
fig = plt.figure(figsize=(20, 10))
i_plot = 1
for feature in df.columns:
    if feature in ['num_bedrooms', 'num_bathrooms', 'area'] or feature in ['furnished', 'utilities_included', "in_unit_laundry", "gym", "parking"]:
        axes = fig.add_subplot(3, 4, i_plot)
        plt.scatter(df[feature], df['rent'])
        axes.set_xlabel(feature)
        axes.set_ylabel("Price")
        axes.set_title("Price vs." + feature)
        i_plot += 1
    if "distance_to_POI:" in feature:
        axes = fig.add_subplot(3, 4, i_plot)
        plt.scatter(df[feature], df['rent'])
        axes.set_xlabel(feature)
        axes.set_ylabel("Price")
        axes.set_title("Price vs." + feature)
        i_plot += 1
# plt.show() # TCUITODO: Re-enable this

# Training dataset and testing dataset:
df_train, df_test, price_train, price_test = train_test_split(df, df['rent'], test_size=0.2)
print(df_train.head(5))
print(df_train.shape, df_train.ndim)
print(price_train)
print(price_train.shape, price_train.ndim)

# TCUITODO: Solve the error `ValueError: Input contains NaN, infinity or a value too large for dtype('float64').`
print(np.any(np.isnan(df_train)), np.any(np.isfinite(df_train)), np.any(np.isnan(price_train)), np.any(np.isfinite(price_train)))

# Train the model:
lin_reg_obj = LinearRegression()
lin_reg_obj.fit(df_train, price_train)
correlations = pd.DataFrame(lreg.coef_, df.columns, columns = ['Coeff'])
print(correlations)
# Test the model:
predictions = lin_reg_obj(df_test)
plt.scatter(price_test, predictions)
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.plot(np.linspace(0,5,100), np.linspace(0,5,100), '-r')
plt.show()
# Visualize the residuals:
plt.hist(price_test - predictions, edgecolor='black')
plt.ylabel("Count")
plt.xlabel("Residual")
plt.show()



# TCUITODO
