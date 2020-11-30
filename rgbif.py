
from pgmagick import Image, ImageList, Geometry, Color,CompositeOperator, Blob,ColorRGB,ColorHSL
import math
from os import path
import requests
import arg_handler

input_gif_path = "input.gif"

output_gif_path = "output.gif"

operator = "color"

emoji = False

minimum_frames = 24

intensity = 1.0

def isLocal(uri):
    if path.isfile(uri):
        return True
    else:
        return False

def scrape(imgURL):
    res = requests.get(imgURL)
    img_data = Blob(res.content)
    return img_data

def extendImageToMinimumFrames(img,min_frames):
    extendedImg = ImageList()
    while len(extendedImg) < min_frames:
        for frame in img:
            extendedImg.append(frame)
    return extendedImg

def rgbFrames(src_imagelist,src_image_size,operator_string,intensity):
    print(intensity,operator_string)
    processed_imagelist = ImageList()
    total_frames = len(src_imagelist)
 
    for (i,frame) in enumerate(src_imagelist):
        percent = float(i)/float(total_frames-1)
        h = 0.5*math.sin(percent*math.pi*2)+0.5
        s = intensity*(0.5*math.sin(percent*math.pi*2*10)+0.5)
        l = 0.25*math.sin(percent*math.pi*4)+0.5

        c = ColorHSL(h,s,l)

        filter = Image(Geometry(src_image_size.columns(),src_image_size.rows()),c)

        if operator_string == "color":
            frame.composite(filter, 0,0,CompositeOperator.ColorizeCompositeOp)
        elif operator_string == "hue": 
            frame.composite(filter, 0,0,CompositeOperator.HueCompositeOp)
        elif operator_string == "overlay":    
            frame.composite(filter, 0,0,CompositeOperator.OverlayCompositeOp)
        elif operator_string == "difference":
            frame.composite(filter, 0,0,CompositeOperator.DifferenceCompositeOp)
        elif operator_string == "dissolve":    
            frame.composite(filter, 0,0,CompositeOperator.DissolveCompositeOp)
        elif operator_string == "multiply":    
            frame.composite(filter, 0,0,CompositeOperator.MultiplyCompositeOp)
           
        frame.transparent(c)
        processed_imagelist.append(frame)

    return processed_imagelist

def creatRGBIF(uri="input.gif",min_frames=24,operation="color",intensity=1,emoji=False,output_path="output.gif"):
    input_gif_imagelist = ImageList()
    input_gif_single_frame = Image()

    #check if input path directs to an existing local file, else interpret the path as an url and retrieve the gif data online
    if not isLocal(uri):
        scraped_data = scrape(uri)
        input_gif_single_frame = Image(scraped_data)
        input_gif_imagelist.readImages(scraped_data)
    else:
        input_gif_single_frame = Image(uri)
        input_gif_imagelist.readImages(uri)

    #extend the gif till it reaches the minimum amount of frames
    if len(input_gif_imagelist) < min_frames:
        input_gif_imagelist = extendImageToMinimumFrames(input_gif_imagelist,min_frames)

    output_gif_imagelist = rgbFrames(input_gif_imagelist,input_gif_single_frame,operation,intensity)

    if emoji:
        output_gif_imagelist.scaleImages(Geometry(48,48))

    if not output_path.endswith(".gif"):
        output_path += ".gif"

    output_gif_imagelist.writeImages(output_path)



if __name__ == "__main__":

    #if this script is ran in a console, assign command line arguments
    my_arg_handler = arg_handler.rgbif_args()

    input_gif_path = my_arg_handler.input_path

    output_gif_path = my_arg_handler.output_path

    operator = my_arg_handler.operator

    emoji = my_arg_handler.emoji

    minimum_frames = my_arg_handler.minimum_frames

    intensity = my_arg_handler.intensity
    #
    creatRGBIF(uri=input_gif_path,min_frames=minimum_frames,operation=operator,intensity=intensity,emoji=emoji,output_path=output_gif_path)
