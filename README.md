## GT Housing Room Availability Data and Visualization

#### Data source: [http://housing.gatech.edu/rooms/FreeRooms.json](http://housing.gatech.edu/rooms/FreeRooms.json) in April 2020, showing search process for 2020-2021 year

#### Data Quality Notes:
- Web scraping didn't start until *after* room-stay selection, and started in the middle of 2nd Year North-Ave self-selection
- North Ave data is therefore incomplete
- Web scraping data might have halted for a bit at some point, no promises. But the timestamps are all there
- Stopped web scraping after the first few days of room selection because I got bored

#### Visualization 1
[![Georgia Tech Housing Search 2020 - Visualization 1](https://img.youtube.com/vi/m7mX-xiZ4rc/0.jpg)](https://youtu.be/m7mX-xiZ4rc)
#### Visualization 2
[![Georgia Tech Housing Search 2020 - Visualization 2](https://img.youtube.com/vi/2aIcVjosz1k/0.jpg)](https://youtu.be/2aIcVjosz1k)  

#### FAQ
**Q: Wouldn't this visualization be better as a webpage than some python Tkinter crap?**    
**A: Yes, go for it.** I suggest looking at using the compressed data; you don't actually need to pickle it, you could just save the timestamps as strings/ints and keep it all in json format  

**Q: What about data for this year? Could you update it in real-time?**  
**A: I mean, probably.** I'm sure there's a way to setup a server to log the data and push it to a github repo automatically, and have a script to compress the data so a webpage could use it. That would be an interesting project, but there are like 2 weeks before room selection and I'm kinda busy.

**Q: Is my Room Selection Number high enough to get the room(s) I want?**  
**A: IDK the answer to that.** I made a document last year where ppl can put their Room Selection Number and Timeslot: [https://docs.google.com/spreadsheets/d/10IjfwrKaCz9sJFydztzRTWKretjQCbet1AT58FXwBes/edit?usp=sharing](https://docs.google.com/spreadsheets/d/10IjfwrKaCz9sJFydztzRTWKretjQCbet1AT58FXwBes/edit?usp=sharing), but there aren't enough data points yet.  Put yours in a comment and we can figure it out, it has to be piecewise linear :)  
Also, keep in mind that this is only partial data for *one* (pretty strange) year, so past data can't really indicate how likely you are to get a spot or not. Even GT Housing has already made some changes, like reserving only a few floors in North Ave buildings for 2nd years instead of entire buildings (probably because the data show that 2nd years didn't fully fill those spots)    
**Additionally, this visualization does not show restrictions on certain rooms for LLCs, undergrad/grad, etc**

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
