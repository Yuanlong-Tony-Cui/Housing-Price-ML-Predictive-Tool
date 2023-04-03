import re

sample = {"address": "6 Airdrie Road, East York, ON", "rent": 2775.0, "num_bedrooms": 2, "num_bathrooms": 1, "furnished": False, "utilities_included": {
    "hydro": True, "wifi": True, "water": False, "heating": True}, "in_unit_laundry": True, "gym": False, "parking": True, "female_only": None, "area": None}
sample2 = {"address": "6 Airdrie Road, East York, ON", "rent": 2775.0, "num_bedrooms": 2, "num_bathrooms": 1, "furnished": False, "utilities_included": {
    "hydro": True, "wifi": True, "water": True, "heating": True}, "in_unit_laundry": True, "parking": True, "female_only": None, "area": None}
sample3 = {"address": "6 Airdrie Road, East York, ON", "rent": 2775.0, "num_bedrooms": 0, "num_bathrooms": None, "furnished": None, "utilities_included": {
    "hydro": True, "wifi": True, "water": False, "heating": True}, "in_unit_laundry": None, "gym": None, "parking": None, "female_only": None, "area": None}
sample4 = {"address": "6 Airdrie Road, East York, ON", "rent": None, "num_bedrooms": 2, "num_bathrooms": 1, "furnished": False, "utilities_included": {
    "hydro": True, "wifi": True, "water": False, "heating": True}, "in_unit_laundry": True, "gym": False, "parking": True, "female_only": None, "area": None}
sample_list = [sample, sample2, sample3, sample4]


def raw_to_cleaned(houses):
    # Remove all data that does not have all of the required keys:
    required_keys = ['address', 'rent', 'num_bedrooms', 'num_bathrooms', 'furnished',
                     'utilities_included', 'in_unit_laundry', 'gym', 'parking', 'female_only', 'area']
    houses = [d for d in houses if all(field in d for field in required_keys)]

    # Remove house that its address dosent start with 0-9
    regex = re.compile(r"^[^0-9]")
    houses = [house for house in houses if not regex.match(house["address"])]

    # Remove house that does not have rent
    houses = [d for d in houses if isinstance(
        d['rent'], float) and d['rent'] > 0]

    # If the utilities field is an object, collapse it into one boolean field.
    for h in houses:
        if isinstance(h['utilities_included'], dict):
            collapsed_bool = True
            for _, v in h['utilities_included'].items():
                if v != True:
                    collapsed_bool = False
                    break
            h['utilities_included'] = collapsed_bool

    # Default values for dicts (aka assumptions)
    for h in houses:
        if h['num_bedrooms'] == 0 or h['num_bedrooms'] is None:
            h['num_bedrooms'] = 1

        if h['num_bathrooms'] == 0 or h['num_bathrooms'] is None:
            h['num_bathrooms'] = 1

        if h['furnished'] != True:
            h['furnished'] = False

        if h['in_unit_laundry'] != True:
            h['in_unit_laundry'] = False

        if h['gym'] != True:
            h['gym'] = False

        if h['parking'] != True:
            h['parking'] = False

        if h['female_only'] != True:
            h['female_only'] = False

    return houses


# print(raw_to_cleaned(sample_list))
