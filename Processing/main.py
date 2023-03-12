from dist_to_campus import dist_to_campus
from dist_to_grocery import dist_to_grocery
import json

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
