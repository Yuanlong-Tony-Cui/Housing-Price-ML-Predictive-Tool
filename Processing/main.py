# from dist_to_campus import dist_to_campus
# from dist_to_grocery import dist_to_grocery
# import json
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

# Load data into a dataframe:
data = open("Processing/sample_dataset.csv", "rb")
df = pd.read_csv(data)
# Summary:
print(df.head(5))
print(df.shape)
print(df.ndim)
print(df.info())
print(df.describe())
# Plots:
plt.hist(df['price'].to_numpy(), bins=10, edgecolor='black')
plt.xlabel('Price')
plt.ylabel('Count')
plt.title('Price Distribution')
plt.tight_layout()
plt.show()
