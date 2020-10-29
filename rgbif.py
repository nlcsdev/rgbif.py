
from pgmagick import Image, ImageList, Geometry, Color,CompositeOperator, Blob
import math
from os import path
import requests
import arg_handler

my_arg_handler = arg_handler.rgbif_args()

#arg_len = len(sys.argv)

input_gif_path = my_arg_handler.input_path
# input_gif_path = r"\Desktop\input.gif"
# if arg_len >= 2:
#     input_gif_path = sys.argv[1].encode('unicode-escape')
#print(base_gif_path)

output_gif_path = my_arg_handler.output_path
# output_gif_path = r"\Desktop\output.gif"
# if arg_len >= 3:
#     output_gif_path = sys.argv[2].encode('unicode-escape')
#print(output_gif_path)

operator = my_arg_handler.operator
# operator = "default"
# if arg_len >= 4:
#     operator = sys.argv[3].encode('ascii').decode('utf-8')

def isLocal(uri):
    if path.isfile(uri):
        return True
    else:
        return False

def scrape(imgURL):
    res = requests.get(imgURL)
    img_data = Blob(res.content)
    return img_data

filterlist = ImageList()
imgs = ImageList()
single_gif = Image()

if not isLocal(input_gif_path):
    scraped_data = scrape(input_gif_path)
    single_gif = Image(scraped_data)
    imgs.readImages(scraped_data)
else:
    single_gif = Image(input_gif_path)
    imgs.readImages(input_gif_path)

total_frames = len(imgs)

def applyRGB(operator_string):
    for (i,frame) in enumerate(imgs):
        percent = i/total_frames
        r = max(1,int(65534*math.sin(percent*math.pi*2)))
        g = max(1,int(65534*-math.sin(percent*math.pi*2)))
        b = max(1,int(65534*-math.cos(percent*math.pi*2)))
        #a = max(0,int(65534*math.sin(percent*math.pi*2)))
        # offsetX = single_gif.columns() - frame.columns()
        # offsetY = single_gif.rows() - frame.rows()
        c = Color(r,g,b)
        filter = Image(Geometry(single_gif.columns(),single_gif.rows()),c)
        if operator == "color":
            frame.composite(filter, 0,0,CompositeOperator.ColorizeCompositeOp)
        elif operator == "hue": 
            frame.composite(filter, 0,0,CompositeOperator.HueCompositeOp)
        elif operator == "overlay":    
            frame.composite(filter, 0,0,CompositeOperator.OverlayCompositeOp)
        elif operator == "diff":
            frame.composite(filter, 0,0,CompositeOperator.DifferenceCompositeOp)
        elif operator == "dissolve":    
            frame.composite(filter, 0,0,CompositeOperator.DissolveCompositeOp)

        frame.composite(filter, 0,0,CompositeOperator.ColorizeCompositeOp)
            
        frame.transparent(c)
        filterlist.append(frame)

if operator == "default":
    applyRGB("color")
    filterlist.writeImages(r"\Desktop\output_color.gif")
    applyRGB("hue")
    filterlist.writeImages(r"\Desktop\output_hue.gif")
else:
    applyRGB(operator)
    filterlist.writeImages(output_gif_path)

#https://cdn.discordapp.com/emojis/726328204373000272.gif?v=1
