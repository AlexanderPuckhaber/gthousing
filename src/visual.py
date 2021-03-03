import tkinter as tk
import os
import time
import json
import datetime as datetime
import pprint
from tkinter import font

from json_parser import add_to_dict

with open(os.path.join(os.getcwd(), "mappings", "building_room_map.json"), 'r') as f:
    building_room_map = json.load(f)


with open(os.path.join(os.getcwd(), "mappings", "file_time_map.json"), 'r') as f:
    file_time_map = json.load(f)

image_output_dir = os.path.join(os.getcwd(), "output_visual", "images")

comparison_json_files = {}

for unix_time in file_time_map.keys():
    with open(os.path.join(os.getcwd(), "data", file_time_map[unix_time]), 'r') as f:
        try:
            json_file = json.load(f)

            comparison_json_file = add_to_dict(json_file)
            comparison_json_files[unix_time] = comparison_json_file
        except:
            print('parse for', unix_time, 'failed!')


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 

animation_window_width=1900
animation_window_height=800

realtime = float(list(comparison_json_files.keys())[0])

play_bool = True

def pause_play(event, play_bool):
    play_bool = not play_bool
    print()


def create_animation_window():
    window = tk.Tk()
    window.title("Tkinter Animation Demo")
    # Uses python 3.6+ string interpolation
    window.geometry(f'{animation_window_width}x{animation_window_height}')


    return window

# Create a canvas for animation and add it to main window
def create_animation_canvas(window):
    canvas = tk.Canvas(window)
    canvas.configure(bg="white")
    canvas.pack(fill="both", expand=True)
    return canvas

def animate(window, canvas, realtime, speed_factor):

    firstWait = True


    timestamps = []
    for unix_time in comparison_json_files.keys():
        timestamps.append(float(unix_time))

    timestamps.sort()

    color_map = {
        0: {"desc": "0/unk", "color": "gray"},
        1: {"desc": "1", "color": "red"},
        2: {"desc": "2", "color": "orange"},
        3: {"desc": "3", "color": "yellow"},
        4: {"desc": "4", "color": "green"},
        5: {"desc": "5", "color": "blue"},
        6: {"desc": "6", "color": "purple"},
        7: {"desc": "7", "color": "pink"},
    }

    for unix_time in timestamps:
        scrape_datetimestamp = datetime.datetime.fromtimestamp(unix_time)

        print(unix_time, scrape_datetimestamp)

        while(realtime < float(unix_time)):
            time.sleep(1/60)
            realtime += speed_factor/60

        window.update()

        # save to file
        canvas.postscript(file=os.path.join(image_output_dir, "{unix_time}.ps".format(unix_time=str(int(unix_time)))))

        # clear canvas
        canvas.delete("all")

        canvas.configure(bg="white")

        height = 50
        boxheight = 30
        boxwidth = 5
        x_offset = 30
        y_offset = 80

        key_x = 225
        key_width = 50

        largeFont = font.Font(family='Helvetica', size=20, weight='bold')
        medFont = font.Font(family='Helvetica', size=15, weight='bold')

        canvas.create_text(key_x + x_offset, 20, text=str(scrape_datetimestamp), font=largeFont)

        canvas.create_text(x_offset, height, anchor="nw", text="Key: # free beds", font=medFont)

        for color_key in color_map.keys():
            canvas.create_text(key_x + x_offset, height, anchor="nw", text=color_map[color_key]["desc"], font=medFont)
            canvas.create_rectangle(key_x + x_offset, height+20, key_x + x_offset+30, height+20 + 30, fill=color_map[color_key]["color"])

            key_x += key_width

        for b_id in building_room_map:
            comp_b_id = -1
            # im a bad person
            compare_json = comparison_json_files[str(int(unix_time))]

            for c_b_id in compare_json:
                if int(c_b_id) == int(b_id):
                    #print("yay! comp b_id: " + str(c_b_id))
                    #print(compare_json[c_b_id])
                    comp_b_id = c_b_id
                else:
                    pass
                    #print("c_b_id", c_b_id, "not found!")

            canvas.create_text(x_offset, height + y_offset, anchor="nw", text=building_room_map[b_id]["BuildingName"], font=medFont)
            x = 225 + x_offset
            #self.canvas.create_rectangle(x, height, x + boxheight, height + boxheight, fill="black")
            #print(b_id)
            #print(compare_json[b_id])
            #print(file_json[b_id]["BuildingName"])

            for apartment in building_room_map[b_id]["Apartments"]:
                #print(apartment)
                old_data = False

                comp_apartment = -1
                # im a bad person
                for c_apartment in compare_json[comp_b_id]["Apartments"]:
                    if int(c_apartment) == int(apartment):
                        #print("yay! comp apt: " + str(c_apartment))
                        #print(compare_json[c_b_id]["Apartments"][c_apartment])
                        comp_apartment = c_apartment
                    else:
                        #print("c_apartment", c_apartment, "not found!")
                        pass
                        #old_data = True

                color="white"

                capacity = building_room_map[b_id]["Apartments"][apartment]["Capacity"]
                num_filled = capacity

                #gender = compare_json[comp_b_id]["Apartments"][comp_apartment][]



                for room in compare_json[comp_b_id]["Apartments"][comp_apartment]["Rooms"]:
                    num_filled -= 1

                    updated_timestamp = compare_json[comp_b_id]["Apartments"][comp_apartment]["Rooms"][room]

                    time_diff = ((scrape_datetimestamp + datetime.timedelta(minutes = 15)) - updated_timestamp)
                    #print(time_diff)

                    if (time_diff > datetime.timedelta(minutes=60)):
                        old_data = True
                    #print("num filled: " + num_filled)

                num_free = capacity - num_filled
                #print(num_free)

                if (old_data):
                    num_free = -42  # special value, see color map

                if num_free in color_map.keys():
                    color = color_map[num_free]["color"]
                else:
                    color = "white"


                #color = _from_rgb((int(255 * (num_filled / capacity)), 255, int(255 * (num_filled / capacity))))

                canvas.create_rectangle(x, height + y_offset, x + boxwidth * capacity, height + y_offset + boxheight, fill=color)

                offset = 0
                for room in range(0, num_filled):
                    #num_filled -= 1
                    #pprint.pprint(room)
                    #print("num filled: " + num_filled)
                    canvas.create_rectangle(x + offset, height + y_offset, x + offset + boxwidth, height + y_offset + boxheight / 4, fill="gray")
                    offset += boxwidth


                x += boxwidth * capacity

            height += boxheight

            if firstWait:
                #time.sleep(20)
                firstWait = False

# The actual execution starts here
animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)
animate(animation_window,animation_canvas, realtime, speed_factor=50000)