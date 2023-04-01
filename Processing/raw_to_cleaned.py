import re

def raw_to_cleaned(houses):
    # Rule 1: remove house that its address dosent start with 0-9
    regex = re.compile(r"^[^0-9]")
    houses = [house for house in houses if not regex.match(house["address"])]

    # Rule 2: if num_bedrooms is null or 0, assume 1
    # Use a list comprehension to create a new list of objects with updated "num_bedrooms" keys
    houses = [{**house, "num_bedrooms": 1} if house["num_bedrooms"] is None or house["num_bedrooms"] == 0 else house for house in houses]

    # testing
    # for house in houses:
    #     print(house["address"])

    return houses
