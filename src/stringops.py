import re

def parse_room_number(r_number):
    match = re.match(r"([a-z]+)([0-9]+)([a-z]+)", r_number, re.I)
    if match:
        items = match.groups()
        return {
            "building_prefix": items[0],
            "room_number": items[1],
            "room_letter": items[2]
        }
    return {
        "building_prefix": "Invalid building prefix!",
            "room_number": "Invalid room number!",
            "room_letter": "Invalid room letter!"
    }

def parse_capacity(r_capacity):
    """Returns int of room capacity based on string input.
    Invalid will return None, not enough info (e.g. \"Suite\") will return -1"""
    match = re.match(r"([0-9]+)", r_capacity, re.I)
    if match:
        return int(match.groups()[0])
    else:
        if r_capacity == "Double":
            return 2
        if r_capacity == "Single":
            return 1
        if r_capacity == "Single Suite":
            return 1
        if r_capacity == "Suite":
            return -1
    print("parse capacity failed!")
    print(r_capacity + ".")
    return -1

print(parse_capacity("6 person"))
print(parse_capacity("Double"))
print(parse_capacity("Suite"))
print(parse_capacity("goop"))