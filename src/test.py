import pprint
import re
import json
from json_parser import add_to_dict
import os

with open(os.path.join(os.getcwd(), "data", "1587537304.json"), 'r') as f:
    file_json = json.load(f)

#pprint.pprint(file_json)

big_dict = add_to_dict(file_json)

pprint.pprint(big_dict, width=200)