
from pgmagick import Image, ImageList, Geometry, Color,CompositeOperator, Blob
import math
from os import path
import requests
import arg_handler
from pygifsicle import optimize

my_arg_handler = arg_handler.rgbif_args()

input_gif_path = my_arg_handler.input_path

output_gif_path = my_arg_handler.output_path

operator = my_arg_handler.operator

minimum_frames = 24

def isLocal(uri):
    if path.isfile(uri):
        return True
    else:
        return False

def scrape(imgURL):
    res = requests.get(imgURL)
    img_data = Blob(res.content)
    return img_data

imgs = ImageList()
single_gif = Image()

if not isLocal(input_gif_path):
    scraped_data = scrape(input_gif_path)
    single_gif = Image(scraped_data)
    imgs.readImages(scraped_data)
else:
    single_gif = Image(input_gif_path)
    imgs.readImages(input_gif_path)



def extendImageToMinimumFrames(img):
    extendedImg = ImageList()
    while len(extendedImg) < minimum_frames:
        for frame in img:
            extendedImg.append(frame)
        #print(len(extendedImg))
    return extendedImg

def applyRGB(operator_string):
    filterlist = ImageList()
    total_frames = len(imgs)
    #print(total_frames)
    for (i,frame) in enumerate(imgs):
        percent = float(i)/float(total_frames-1)
        sR = 0.5*math.sin(percent*math.pi*2)+0.5
        sG = -0.5*math.sin(percent*math.pi*2)+0.5
        sB = 0.5*math.sin(percent*math.pi*4)+0.5
        maxRGB = 65535
        r = max(1,int(maxRGB*sR))
        g = max(1,int(maxRGB*sB))
        b = max(1,int(maxRGB*sG))
        c = Color(r,g,b)
        
        filter = Image(Geometry(single_gif.columns(),single_gif.rows()),c)
        
        if operator_string == "color":
            frame.composite(filter, 0,0,CompositeOperator.ColorizeCompositeOp)
        elif operator_string == "hue": 
            frame.composite(filter, 0,0,CompositeOperator.HueCompositeOp)
        elif operator_string == "overlay":    
            frame.composite(filter, 0,0,CompositeOperator.OverlayCompositeOp)
        elif operator_string == "diff":
            frame.composite(filter, 0,0,CompositeOperator.DifferenceCompositeOp)
        elif operator_string == "dissolve":    
            frame.composite(filter, 0,0,CompositeOperator.DissolveCompositeOp)
           
        frame.transparent(c)
        filterlist.append(frame)
    return filterlist

if len(imgs) < minimum_frames:
    imgs = extendImageToMinimumFrames(imgs)

if operator == "default":
    applyRGB("color").writeImages(r"\Desktop\output_color.gif")
    #optimize(r"\Desktop\output_color.gif")
    applyRGB("hue").writeImages(r"\Desktop\output_hue.gif")
    #optimize(r"\Desktop\output_hue.gif")
else:
    applyRGB(operator).writeImages(output_gif_path)
    #optimize(output_gif_path)

#https://cdn.discordapp.com/emojis/726328204373000272.gif?v=1
