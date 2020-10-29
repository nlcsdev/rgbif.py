import argparse
import sys

parse = argparse.ArgumentParser()
parse.add_argument("-o",default="default")
#parse.add_argument("-color","-hue","-overlay","-diff","-dissolve")
parse.add_argument("-out",nargs= 1,default=["\\Desktop\\output.gif"])
parse.add_argument("-input",nargs=1,default=[r"\Desktop\input.gif"])

class rgbif_args():
    global parse
    input_path = r"\Desktop\input.gif"
    operator = "default"
    output_path = "\\Desktop\\output_{0}.gif"
    
    def __init__(self):
        args = parse.parse_args()
        #print(args)
        self.input_path = args.input[0]
        #print(self.input_path)
        self.operator = args.o
        #print(self.operator)
        self.output_path = args.out[0].format(self.operator)
        #print(self.output_path)
        