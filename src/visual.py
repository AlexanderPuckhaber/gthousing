import tkinter as tk
import os
import json
import pprint
from json_parser import add_to_dict

with open(os.path.join(os.getcwd(), "output", "output.json"), 'r') as f:
    file_json = json.load(f)

#pprint.pprint(file_json)


# this is the comparison file, change this. i want to make a time slider soon...
with open(os.path.join(os.getcwd(), "data", "1587694016.json"), 'r') as f:
    compare_json_file = json.load(f)

compare_json = add_to_dict(compare_json_file)

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 


class Example(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(self, width=400, height=800)
        self.canvas.pack(side="top", fill="both", expand=True)

        # draw some items
        #self.canvas.create_rectangle(50,50,150,150, fill="red")
        #self.canvas.create_oval(20,20,65, 75, outline="green")
        #self.canvas.create_text(10,200, anchor="nw", text="Hello, world")

        height = 50
        boxheight = 30
        boxwidth = 5

        for b_id in file_json:
            comp_b_id = -1
            # im a bad person
            for c_b_id in compare_json:
                if int(c_b_id) == int(b_id):
                    print("yay! comp b_id: " + str(c_b_id))
                    #print(compare_json[c_b_id])
                    comp_b_id = c_b_id
                

            self.canvas.create_text(0, height, anchor="nw", text=file_json[b_id]["BuildingName"])
            x = 150
            #self.canvas.create_rectangle(x, height, x + boxheight, height + boxheight, fill="black")
            #print(b_id)
            #print(compare_json[b_id])
            #print(file_json[b_id]["BuildingName"])

            for apartment in file_json[b_id]["Apartments"]:
                #print(apartment)

                comp_apartment = -1
                # im a bad person
                for c_apartment in compare_json[comp_b_id]["Apartments"]:
                    if int(c_apartment) == int(apartment):
                        print("yay! comp apt: " + str(c_apartment))
                        print(compare_json[c_b_id]["Apartments"][c_apartment])
                        comp_apartment = c_apartment
                

                color="white"

                
                capacity = file_json[b_id]["Apartments"][apartment]["Capacity"]
                num_filled = capacity


                for room in compare_json[comp_b_id]["Apartments"][comp_apartment]["Rooms"]:
                    num_filled -= 1
                    pprint.pprint(room)
                    #print("num filled: " + num_filled)


                num_free = capacity - num_filled
                #print(num_free)

                if (num_free == 0):
                    color = "white"
                elif (num_free == 1):
                    color = "red"
                elif (num_free == 2):
                    color = "orange"
                elif (num_free == 3):
                    color = "yellow"
                elif (num_free == 4):
                    color = "green"
                elif (num_free == 5):
                    color = "blue"
                elif (num_free == 6):
                    color = "purple"
                elif (num_free == 7):
                    color = "pink"
                else:
                    color = "black"

                if comp_apartment == -1:
                    color = "gray"


                #color = _from_rgb((int(255 * (num_filled / capacity)), 255, int(255 * (num_filled / capacity))))

                self.canvas.create_rectangle(x, height, x + boxwidth * capacity, height + boxheight, fill=color)

                offset = 0
                for room in range(0, num_filled):
                    #num_filled -= 1
                    #pprint.pprint(room)
                    #print("num filled: " + num_filled)
                    self.canvas.create_rectangle(x + offset, height, x + offset + boxwidth, height + boxheight / 4, fill="gray")
                    offset += boxwidth    


                x += boxwidth * capacity

            height += boxheight

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()