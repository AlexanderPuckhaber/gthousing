from stringops import parse_room_number, parse_capacity
import pprint
import datetime

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

        vividict[b_id]["Apartments"][r_number]["Rooms"][r_letter] = datetime.datetime.strptime(r_last_updated, "%Y-%m-%d %H:%M:%S")

        #vividict[b_id]["Apartments"][r_number]["Rooms"][r_letter]["Changelog"] 

        # fix capacity if it was invalid
        if r_capacity < 0:
            r_capacity = 0
            for room in vividict[b_id]["Apartments"][r_number]["Rooms"]:
                r_capacity += 1
            vividict[b_id]["Apartments"][r_number]["Capacity"] = r_capacity
    
    return vividict

def add_to_dict2(json_file, vividict, scrape_timestamps):

    for room_entry in json_file:
        #pprint.pprint(room_entry)

        b_id = room_entry["BuildingID"]
        b_name = room_entry["BuildingName"]
        r_number_parsed = parse_room_number(room_entry["RoomNumber"])
        r_number = r_number_parsed["room_number"]
        r_letter = r_number_parsed["room_letter"]

        r_capacity = parse_capacity(room_entry["Capacity"])
        r_gender = room_entry["Gender"]
        r_term = room_entry["Term"]

        r_last_updated = room_entry["LastUpdated"]


        vividict[b_id]["BuildingName"] = b_name
        curr_appt = vividict[b_id]["Apartments"][r_number]
        curr_appt["Capacity"] = r_capacity

        timestamp_current = datetime.datetime.strptime(r_last_updated, "%Y-%m-%d %H:%M:%S")

        curr_room = vividict[b_id]["Apartments"][r_number]["Rooms"][r_letter]

        # TODO: FIX
        if "UpdateLog" in curr_room.keys():
            # find latest timestamp before now
            #print('keys', curr_room["UpdateLog"].keys())
            #latest_updatelog = max(dt for dt in curr_room["UpdateLog"].keys() if dt < timestamp_current)
            latest_updatelog_key = max(curr_room["UpdateLog"].keys())
            latest_updatelog = curr_room["UpdateLog"][latest_updatelog_key]
            #print(latest_updatelog)

            # find previous scrape timestamp
            latest_scrape_timestamp = max(ts for ts in scrape_timestamps if ts < timestamp_current)

            # we scrape every 10 minutes, longer than this would be expired data
            expiration_time = datetime.timedelta(minutes=20)

            # check time since last updatelog
            #print('timedelta',  timestamp_current - latest_updatelog["to"])
            if latest_updatelog["to"] >= (latest_scrape_timestamp - expiration_time):
                # recent enough, keep log entry and extend "to" timestamp
                curr_room["UpdateLog"][latest_updatelog_key]["to"] = timestamp_current
                curr_room["UpdateLog"][latest_updatelog_key]["Gender"] = r_gender
            else:
                # expired, create new entry
                curr_room["UpdateLog"][timestamp_current] = {
                    "from": timestamp_current,
                    "to": timestamp_current,
                    "Gender": r_gender
                }

        else:
            # mark available at this timestamp
            curr_room["UpdateLog"][timestamp_current] = {
                "from": timestamp_current,
                "to": timestamp_current,
                "Gender": r_gender
            }

        curr_room["Term"] = r_term
        curr_room["Room Number"] = r_number
        curr_room["Room Letter"] = r_letter

        # fix capacity if it was invalid
        if r_capacity < 0:
            r_capacity = 0
            for room in vividict[b_id]["Apartments"][r_number]["Rooms"]:
                r_capacity += 1
            # only overwrite if we found more
            if r_capacity > vividict[b_id]["Apartments"][r_number]["Capacity"]:
                vividict[b_id]["Apartments"][r_number]["Capacity"] = r_capacity

    # pprint.pprint(vividict)

    return vividict
