import os
import json
from structures import Room, Apartment, Building
from stringops import parse_room_number, parse_capacity
import pprint

#data folder directory
data_dir = os.path.join(os.getcwd(), 'data')

print(data_dir)

json_list = []

building_set = set([])

for filename in os.listdir(data_dir):
    print(filename)
    with open(os.path.join(data_dir, filename), 'r') as f:
        print(filename)
        try:
            file_json = json.load(f)
            json_list.append(file_json)
        except:
            print(filename + " has invalid content")

print("json_list length: " + str(len(json_list)))

test_room = Room(letter="A", term="2020 Fall", last_updated="2020-04-22 08:02:09")
print(test_room)

print(json_list[0][0])
print(json_list[0][0]["BuildingID"])
print(json_list[0][0]["BuildingName"])
print(json_list[0][0]["RoomNumber"])



class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

vividict = Vividict()

for curr_json in json_list:
    for room_entry in curr_json:
        b_id = room_entry["BuildingID"]
        b_name = room_entry["BuildingName"]
        r_number_parsed = parse_room_number(room_entry["RoomNumber"])

        r_number = r_number_parsed["room_number"]
        r_letter = r_number_parsed["room_letter"]

        r_capacity = parse_capacity(room_entry["Capacity"])

        r_last_updated = room_entry["LastUpdated"]

        

        vividict[b_id]["BuildingName"] = b_name
        vividict[b_id]["Apartments"][r_number]["Capacity"] = r_capacity

        vividict[b_id]["Apartments"][r_number]["Rooms"][r_letter] = r_last_updated

        # fix capacity if it was invalid
        if r_capacity < 0:
            r_capacity = 0
            for room in vividict[b_id]["Apartments"][r_number]["Rooms"]:
                r_capacity += 1
            vividict[b_id]["Apartments"][r_number]["Capacity"] = r_capacity


output_json = json.dumps(vividict)

# write output json
with open(os.path.join(os.path.join(os.getcwd(), "output"), "output.json"), "w") as f:
    f.write(output_json)


pprint.pprint(vividict, width=180)



