# from dist_to_campus import dist_to_campus
# from dist_to_grocery import dist_to_grocery
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
def preprocess_dataset(arg_data):
    i_row = 0
    while i_row < len(arg_data):
        features = list(arg_data[i_row].keys())
        for feature in features:
            if feature == "rent" and arg_data[i_row][feature] == None:
                arg_data[i_row][feature] = 0
            if feature in ['furnished', 'utilities_included', "in_unit_laundry", "gym", "parking"]:
                if arg_data[i_row][feature] == True:
                    arg_data[i_row][feature] = "True"
                elif arg_data[i_row][feature] == False:
                    arg_data[i_row][feature] = "False"
                else:
                    arg_data[i_row][feature] = "Unknown"
            if feature == "distance_to_POI":
                for poi in arg_data[i_row][feature]:
                    if poi != "bus_stop": # TCUITODO: Handle "bus_stop"
                        new_key = feature + ":" + poi
                        arg_data[i_row][new_key] = arg_data[i_row][feature][poi]
        i_row += 1
    print("arg_data[0]:", arg_data[0])
    return arg_data

df = pd.DataFrame(preprocess_dataset(data))

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
plt.show()

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
plt.show()
