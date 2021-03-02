import os
import json

file_time_map = {}

directory = os.path.join(os.getcwd(), "data")
for entry in os.scandir(directory):
    if (entry.path.endswith(".json")):
        filename = os.path.basename(entry.path)
        filename_parts = filename.split('.')
        unix_timestamp = int(filename_parts[0])

        file_time_map[unix_timestamp] = filename

print(file_time_map)

output_json = json.dumps(file_time_map)

# write output json
with open(os.path.join(os.path.join(os.getcwd(), "mappings"), "file_time_map.json"), "w") as f:
    f.write(output_json)