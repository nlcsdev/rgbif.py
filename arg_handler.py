import argparse
import sys

parse = argparse.ArgumentParser()
parse.add_argument("-o",default="color")
parse.add_argument("-emoji",nargs='?',const=True,default=False)
parse.add_argument("-i",type=float,default=1.0)
parse.add_argument("-minframes",type=int,default=24)
parse.add_argument("-output",default="\\Desktop\\output_{0}.gif")
parse.add_argument("-input",default=r"\Desktop\input.gif")

class rgbif_args():
    global parse
    input_path = r"\Desktop\input.gif"
    operator = "color"
    output_path = "\\Desktop\\output_{0}.gif"
    emoji = False
    intensity = 1.0
    minimum_frames = 24
    
    def __init__(self):
        args = parse.parse_args()
        self.operator = args.o
        self.emoji = args.emoji
        self.intensity = args.i
        self.minimum_frames = args.minframes
        self.input_path = args.input
        self.output_path = args.output.format(self.operator)
        