
from pgmagick import Image, ImageList, Geometry, Color,CompositeOperator, Blob,ColorRGB,ColorHSL
import math
from os import path
import requests
import arg_handler
from pygifsicle import optimize

my_arg_handler = arg_handler.rgbif_args()

input_gif_path = my_arg_handler.input_path

output_gif_path = my_arg_handler.output_path

operator = my_arg_handler.operator

emoji = my_arg_handler.emoji

minimum_frames = my_arg_handler.minimum_frames

intensity = my_arg_handler.intensity

imgs = ImageList()
single_gif = Image()

def isLocal(uri):
    if path.isfile(uri):
        return True
    else:
        return False

def scrape(imgURL):
    res = requests.get(imgURL)
    img_data = Blob(res.content)
    return img_data

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
        sH = 0.5*math.sin(percent*math.pi*2)+0.5
        sS = 0.5*intensity*math.sin(percent*math.pi*2*10)+0.5
        sL = 0.25*math.sin(percent*math.pi*4)+0.5
        #
        h = sH
        s = sS
        l = sL
        c = ColorHSL(h,s,l)

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
        elif operator_string == "multiply":    
            frame.composite(filter, 0,0,CompositeOperator.MultiplyCompositeOp)
           
        frame.transparent(c)
        filterlist.append(frame)
    return filterlist

if __name__ == "__main__":
    if not isLocal(input_gif_path):
        scraped_data = scrape(input_gif_path)
        single_gif = Image(scraped_data)
        imgs.readImages(scraped_data)
    else:
        single_gif = Image(input_gif_path)
        imgs.readImages(input_gif_path)

    if len(imgs) < minimum_frames:
        imgs = extendImageToMinimumFrames(imgs)

    if operator == "default":
        new_gif_color = applyRGB("color")
        new_gif_hue = applyRGB("hue")
        #
        if emoji:
            new_gif_color.scaleImages(Geometry(48,48))
            new_gif_hue.scaleImages(Geometry(48,48))
        #
        new_gif_color.writeImages(r"\Desktop\output_color.gif")
        new_gif_hue.writeImages(r"\Desktop\output_hue.gif")
        #
        #optimize(r"\Desktop\output_color.gif")
        #optimize(r"\Desktop\output_hue.gif")
    else:
        new_gif = applyRGB(operator)
        #
        if emoji:
            new_gif.scaleImages(Geometry(48,48))
        #
        new_gif.writeImages(output_gif_path)
        #
        #optimize(output_gif_path)