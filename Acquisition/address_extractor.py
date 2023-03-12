import re
import json

def address_extractor(json_name):
    # Load the input data from JSON file
    with open(json_name, 'r') as f:
        input_data = json.load(f)

    # Extract the addresses from the input data
    texts = input_data['texts']

    # Define a regular expression pattern to match addresses
    pattern = r'\b\d+\s+\w+\s+(?:street|st|avenue|ave|road|rd|boulevard|blvd|lane|ln|drive|dr)\b'

    results = []
    for text in texts:
        # Use the pattern to search for matches in the text
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            results.append(matches[0])

    return results
