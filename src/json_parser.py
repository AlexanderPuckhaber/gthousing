from stringops import parse_room_number, parse_capacity
import pprint
from datetime import *

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def add_to_dict(json_file):
    

    vividict = Vividict()


    for room_entry in json_file:
        #pprint.pprint(room_entry)
        b_id = room_entry["BuildingID"]
        b_name = room_entry["BuildingName"]
        r_number_parsed = parse_room_number(room_entry["RoomNumber"])

        r_number = r_number_parsed["room_number"]
        r_letter = r_number_parsed["room_letter"]

        r_capacity = parse_capacity(room_entry["Capacity"])

        r_last_updated = room_entry["LastUpdated"]


        vividict[b_id]["BuildingName"] = b_name
        vividict[b_id]["Apartments"][r_number]["Capacity"] = r_capacity

        vividict[b_id]["Apartments"][r_number]["Rooms"][r_letter] = datetime.strptime(r_last_updated, "%Y-%m-%d %H:%M:%S")

        #vividict[b_id]["Apartments"][r_number]["Rooms"][r_letter]["Changelog"] 

        # fix capacity if it was invalid
        if r_capacity < 0:
            r_capacity = 0
            for room in vividict[b_id]["Apartments"][r_number]["Rooms"]:
                r_capacity += 1
            vividict[b_id]["Apartments"][r_number]["Capacity"] = r_capacity
    
    return vividict
    