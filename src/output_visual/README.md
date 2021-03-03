### How to make visuals

The code in visual.py outputs the tkinter canvas frames as postscript `.ps` files in the [/images/](/images/) folder.

To convert the `.ps` files to `.png` files, I used this `mogrify`:  
`mogrify -path png_output/ -format png -background white -alpha remove -alpha off -colorspace RGB images/*.ps`

Then, to convert to a `.mp4` video, I used `ffmpeg`:  
`ffmpeg -r 60 -s 1441x783 -pattern_type glob -i 'png_output/*.png' -c:v libx264rgb visual.mp4`