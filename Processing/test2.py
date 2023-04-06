from raw_to_cleaned import raw_to_cleaned
from dist_to_campus import dist_to_campus
from dist_to_POI import dist_to_POI
import json
import os

# Load the input data from JSON file
dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(dir, '../Acquisition/housing_data.json'), 'r') as f:
    houses_raw = json.load(f)

# clean the data and save as json
# houses_cleaned = raw_to_cleaned(houses_raw)

# load cleaned data
with open(os.path.join(dir, '../Processing/housing_data_cleaned.json'), 'r') as f:
    houses_cleaned = json.load(f)

# trim data to keep the first 999 entries confronting the limit given from API policy
houses_cleaned = houses_cleaned[0:10]

# Extract the addresses from the input data (same order)
addresses = [house['address'] for house in houses_cleaned]

# Call functions with the addresses as input
campus_distances = dist_to_campus(addresses, True)
grocery_distances = dist_to_POI(addresses, True, "grocery")
# bus_stop_distances = dist_to_POI(addresses,False,"bus")

# Use a list comprehension to create a new list of objects with "distance_to_POI" keys added
houses_processed = [
    {**house, "distance_to_POI": {
        "campus": campus_distances[i],
        "grocery": grocery_distances[i],
        # "bus_stop": bus_stop_distances[i]
        "bus_stop": "pending"
    }} for i, house in enumerate(houses_cleaned)
]

with open(os.path.join(dir, 'housing_data_processed.json'), "w") as outfile:
    # Write the JSON object to the file
    json.dump(houses_processed, outfile)
