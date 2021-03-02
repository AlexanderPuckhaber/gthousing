import pprint
import datetime
import re
import json
from json_parser import add_to_dict, add_to_dict2, Vividict
import os
import pickle

with open(os.path.join(os.getcwd(), "data", "1587537304.json"), 'r') as f:
    file_json = json.load(f)

#pprint.pprint(file_json)


with open(os.path.join(os.getcwd(), "mappings", "file_time_map.json"), 'r') as f:
    file_time_map = json.load(f)

comparison_json_files = {}

limit = 4000

next_vividict = next_vividict = Vividict()
sorted_time_map_keys = sorted(file_time_map.keys())

scrape_timestamps = []
for scrape_time in sorted_time_map_keys:
    scrape_timestamps.append(datetime.datetime.fromtimestamp(int(scrape_time)))

for unix_time in sorted_time_map_keys:
    with open(os.path.join(os.getcwd(), "data", file_time_map[unix_time]), 'r') as f:
        try:
            json_file = json.load(f)

        except:
            print('parse for', unix_time, 'failed!')

        next_vividict = add_to_dict2(json_file, next_vividict, scrape_timestamps)
        # pprint.pprint(next_vividict, width=200)

    limit = limit -1
    if limit <= 0:
        break

pprint.pprint(next_vividict)

# write output
with open(os.path.join(os.path.join(os.getcwd(), "mappings"), "big_dict.pickle"), "wb") as f:
    pickle.dump(next_vividict, f)