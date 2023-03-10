from dist_to_campus import dist_to_campus
import json

# Load the input data from JSON file
with open('Processing/sample_addresses.json', 'r') as f:
    input_data = json.load(f)

# Extract the addresses from the input data
addresses = input_data['addresses']

# Call the dist_to_campus function with the addresses as input
distances = dist_to_campus(addresses,True)

# Print the distances
print(distances)
