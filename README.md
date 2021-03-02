## GT Housing Room Availability Data and Visualization

#### Data source: [http://housing.gatech.edu/rooms/FreeRooms.json](http://housing.gatech.edu/rooms/FreeRooms.json)

#### Data Quality Notes:
- Web scraping didn't start until *after* room-stay selection, and started in the middle of 2nd Year North-Ave self-selection
- North Ave data is therefore incomplete
- Web scraping data might have halted for a bit at some point, no promises. But the timestamps are all there
- Stopped web scraping after the first few days of room selection because I got bored

#### How to run?
The data is already generated, so just `cd src/` and run:  
`python visual.py`  
or  
`python visual2.py`

#### What about the other files?
- [src/web_scraper/getjson.sh](src/web_scraper/getjson.sh) is a bash script I used to get the data every 10 minutes
- [src/data/](src/data/) holds all the data I recorded
- [/src/file_time_mapper.py](/src/file_time_mapper.py) maps the web-scrape filenames to timestamps
- [/src/generate_building_room_map.py](/src/generate_building_room_map.py) makes a mapping of all the buildings and rooms that appeared throughout the web-scraping: [/src/mappings/building_room_map.json](/src/mappings/building_room_map.json)
- [/src/visual.py](/src/visual.py) naively goes through all the web-scraped jsons, maps them into [/src/mappings/building_room_map.json](/src/mappings/building_room_map.json), and prints the output on a Tkinter canvas
- [/src/json_parser.py](/src/json_parser.py) and [/src/test.py](/src/test.py) compress all the web-scraped data by generating an "UpdateLog" of when each room appears and disappears in the web-scraped jsons. The output is put into a python pickle file, [/src/mappings/big_dict.pickle](/src/mappings/big_dict.pickle)
- [/src/visual2.py](/src/visual2.py) is similar to [/src/visual.py](/src/visual.py), except it uses the compressed data [/src/mappings/big_dict.pickle](/src/mappings/big_dict.pickle) and has some visual changes
