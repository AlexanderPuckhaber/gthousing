import tkinter as tk
import os
import time
import json
import datetime as datetime
import pprint
from tkinter import font
from json_parser import add_to_dict, add_to_dict2, Vividict
import pickle
import bisect

from json_parser import add_to_dict

with open(os.path.join(os.getcwd(), "mappings", "building_room_map.json"), 'r') as f:
    building_room_map = json.load(f)


with open(os.path.join(os.getcwd(), "mappings", "file_time_map.json"), 'r') as f:
    file_time_map = json.load(f)

image_output_dir = os.path.join(os.getcwd(), "output_visual2", "images")

limit = 4000

next_vividict = next_vividict = Vividict()
sorted_time_map_keys = sorted(file_time_map.keys())

scrape_timestamps = []
for scrape_time in sorted_time_map_keys:
    scrape_timestamps.append(datetime.datetime.fromtimestamp(int(scrape_time)))

big_dict = None

with open(os.path.join(os.getcwd(), "mappings", "big_dict.pickle"), 'rb') as f:
    big_dict = pickle.load(f)

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 

animation_window_width=1900
animation_window_height=850

realtime_start = min(scrape_timestamps)
realtime_end = max(scrape_timestamps)
realtime = realtime_start

def create_animation_window():
    window = tk.Tk()
    window.title("Fall 2020 Housing Self-Assignments")
    # Uses python 3.6+ string interpolation
    window.geometry(f'{animation_window_width}x{animation_window_height}')
    return window

# Create a canvas for animation and add it to main window
def create_animation_canvas(window):
    canvas = tk.Canvas(window)
    canvas.configure(bg="white")
    canvas.pack(fill="both", expand=True)
    return canvas

def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect.bisect_right(a, x)
    if i:
        return a[i-1]
    return None

def animate(window, canvas, realtime_start, realtime_end, speed_factor):

    firstWait = True

    color_map = {
        0: {"desc": "0/?", "color": "gray"},
        1: {"desc": "1", "color": "red"},
        2: {"desc": "2", "color": "orange"},
        3: {"desc": "3", "color": "yellow"},
        4: {"desc": "4", "color": "green"},
        5: {"desc": "5", "color": "blue"},
        6: {"desc": "6", "color": "purple"},
        7: {"desc": "7", "color": "pink"},
    }

    gender_color_map = {
        "Female": "pink",
        "Male": "blue",
        "null": "gray",
        "Dynamic": "gray",
        None: "gray"
    }

    realtime = realtime_start

    last_scrape_timestamp = find_le(scrape_timestamps, realtime)

    while realtime >= realtime_start and realtime <= realtime_end:

        while find_le(scrape_timestamps, realtime) is last_scrape_timestamp:
            time.sleep(1/60)
            realtime += datetime.timedelta(seconds=speed_factor/60)

        scrape_timestamp = find_le(scrape_timestamps, realtime)
        last_scrape_timestamp = scrape_timestamp

        window.update()

        canvas.postscript(file=os.path.join(image_output_dir, "{unix_time}.ps".format(unix_time=str(scrape_timestamp))))
        # clear canvas
        canvas.delete("all")

        height = 50
        boxheight = 30
        boxwidth = 5
        x_offset = 30
        y_offset = 80

        key_x = 200
        key_width = 50

        largeFont = font.Font(family='Helvetica', size=20, weight='bold')
        medFont = font.Font(family='Helvetica', size=16)



        canvas.create_text(x_offset, height, anchor="nw", text="Key: # free beds", font=medFont)

        for color_key in color_map.keys():
            canvas.create_text(key_x + x_offset, height, anchor="nw", text=color_map[color_key]["desc"], font=medFont)
            canvas.create_rectangle(key_x + x_offset, height+20, key_x + x_offset+30, height+20 + 30, fill=color_map[color_key]["color"])

            key_x += key_width

        canvas.create_text(key_x + x_offset + 50, height, anchor="nw",
                           text="Bed Color = Gender\nGrouped by floor increasing left to right", font=medFont)

        canvas.create_text(key_x + x_offset + 550, height, anchor="nw", text=str(scrape_timestamp), font=largeFont)

        for b_id in big_dict:

            canvas.create_text(x_offset, height + y_offset, anchor="nw", text=big_dict[b_id]["BuildingName"],
                               font=medFont)
            x = 200 + x_offset

            apartment_ids = big_dict[b_id]["Apartments"].keys()

            sorted_apartment_ids = sorted(apartment_ids)
            print(sorted_apartment_ids)

            last_floor = "1"

            for apartment_id in sorted_apartment_ids:
                apartment = big_dict[b_id]["Apartments"][apartment_id]

                color="white"

                capacity = apartment["Capacity"]
                num_filled = capacity
                prev_num_filled = capacity
                use_prev = False
                any_found = False

                #gender = compare_json[comp_b_id]["Apartments"][comp_apartment][]
                r_gender = "Dynamic"

                for room_id in apartment["Rooms"]:
                    room = apartment["Rooms"][room_id]
                    #print('room', room)
                    current_floor = room["Room Number"][0]
                    # check if room is within UpdateLogs

                    latest_updatelog_id = find_le(sorted(room["UpdateLog"].keys()), realtime)
                    last_room_scrape = realtime_start
                    if latest_updatelog_id is not None:
                        latest_updatelog = room["UpdateLog"][latest_updatelog_id]
                        # check if we are within range
                        if realtime >= latest_updatelog["from"] and realtime <= latest_updatelog["to"]:
                            # we are within range (data says room currently available)
                            num_filled -= 1
                            r_gender = latest_updatelog["Gender"]
                            any_found = True
                        elif realtime >= latest_updatelog["from"]:
                            r_gender = latest_updatelog["Gender"]
                            use_prev = True
                            if latest_updatelog["to"] > last_room_scrape:
                                last_room_scrape = latest_updatelog["to"]
                                prev_num_filled = capacity
                            if latest_updatelog["to"] == last_room_scrape:
                                prev_num_filled -= 1
                        else:
                            # room is currently not available
                            pass
                    else:
                        # assume filled
                        num_filled = capacity

                num_free = capacity - num_filled

                if any_found:
                    use_prev = False

                if num_free in color_map.keys():
                    color = color_map[num_free]["color"]
                else:
                    color = "white"

                #color = _from_rgb((int(255 * (num_filled / capacity)), 255, int(255 * (num_filled / capacity))))
                print(current_floor)

                if current_floor is not last_floor:
                    x += 10

                    last_floor = current_floor


                if (use_prev):
                    # canvas.create_oval(x, height + y_offset, x + boxwidth * capacity, height + y_offset + boxheight,
                    #                      fill=color_map[capacity - prev_num_filled]["color"])
                    pass
                    # canvas.create_rectangle(x, height + y_offset, x + boxwidth * capacity, height + y_offset + boxheight*0.5,
                    #                     fill=color_map[capacity - prev_num_filled]["color"])
                    canvas.create_rectangle(x, height + y_offset, x + boxwidth * capacity,
                                            height + y_offset + boxheight * 0.5,
                                            fill="gray")
                    pass
                else:
                    canvas.create_rectangle(x, height + y_offset, x + boxwidth * capacity,
                                            height + y_offset + boxheight,
                                            fill=color)

                offset = 0
                for room in range(0, num_filled):

                    canvas.create_rectangle(x + offset, height + y_offset, x + offset + boxwidth,
                                            height + y_offset + boxheight / 4, fill=gender_color_map[r_gender])

                    offset += boxwidth


                x += boxwidth * capacity

            height += boxheight + 10

            if firstWait:
                #time.sleep(5)
                firstWait = False

# The actual execution starts here
animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)
animate(animation_window,animation_canvas, realtime_start, realtime_end, speed_factor=50000)