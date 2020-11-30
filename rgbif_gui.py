from tkinter import *
from tkinter import filedialog
from rgbif import input_gif_path, output_gif_path, operator,emoji, minimum_frames, intensity,creatRGBIF
import os

supported_file_types = [
    ("All Format",".*"),
    ("BMP",".bmp"),
    ("GIF",".gif"),
    ("JPEG",".jpeg"),
    ("JPEG",".jpg"),
    ("MNG",".mng"),
    ("MIFF",".miff"),
    ("PNG",".png"),
    ("TIFF",".tiff"),
    ("TIFF",".tif"),
]

def browse_file():
    return filedialog.askopenfilename(parent=root,initialdir=os.getcwd(),filetypes=supported_file_types)

def save_as():
    return filedialog.asksaveasfilename(parent=root,initialdir=os.getcwd(),filetypes=[("GIF",".gif")])

if __name__ == "__main__":

    root = Tk()

    root.title("rgbif.exe")

    #input GUI
    input_gif_path_var = StringVar()
    input_gif_path_var.set("input.gif")
    input_gif_path_gui_dir_field = Entry(root, text=input_gif_path_var)
    input_gif_path_gui_dir_field.grid(row=0,column=0,columnspan=10,sticky=W+E,padx=10,pady=10)

    inputput_gif_path_browse_btn = Button(root,width=15,text="Select Input",command=lambda : input_gif_path_var.set(browse_file()))
    inputput_gif_path_browse_btn.grid(row=0,column=11,sticky=E,padx=5,pady=10)
    #

    #output GUI
    output_gif_path_var = StringVar()
    output_gif_path_var.set("output.gif")
    output_gif_path_gui_dir_field = Entry(root, text=output_gif_path_var)
    output_gif_path_gui_dir_field.grid(row=1,column=0,columnspan=10,padx=10,sticky=W+E,pady=10)

    output_gif_path_browse_btn = Button(root,width = 15,text="Select Output",command=lambda : output_gif_path_var.set(save_as()))
    output_gif_path_browse_btn.grid(row=1,column=11,sticky=E,padx=5,pady=10)
    #

    #operator GUI
    operator_options=[
        "color",
        "hue",
        "overlay",
        "difference",
        "dissolve",
        "multiply"
    ]

    operator_var = StringVar()
    operator_var.set(operator_options[0])

    operator_label = Label(root,text="Operations")
    operator_label.grid(row=2,column=0,sticky=W,padx=5,pady=5)

    operator_gui_dropdown_value = OptionMenu(root,operator_var,*operator_options)
    operator_gui_dropdown_value.grid(row=2,column=1,sticky=W,pady=5)
    #
    
    #other options GUI
    minimum_frames_label = Label(root,text="minimum frames")
    minimum_frames_label.grid(row=3,column=0,sticky=W,padx=5,pady=5)

    minimum_frames_gui_input_field = Entry(root,width=5)
    minimum_frames_gui_input_field.insert(0,24)
    minimum_frames_gui_input_field.grid(row=3,column=1,columnspan=1,sticky=W,pady=5)

    intensity_label = Label(root,text="intensity")
    intensity_label.grid(row=3,column=2,sticky=W,padx=5,pady=5)

    intensity_gui_input_field = Entry(root,width=5)
    intensity_gui_input_field.insert(0,1.0)
    intensity_gui_input_field.grid(row=3,column=3,columnspan=1,sticky=W,pady=5)

    emoji_var = BooleanVar()
    emoji_label = Label(root,text="emoji")
    emoji_label.grid(row=3,column=4,sticky=W,padx=5,pady=5)

    emoji_gui_toggle = Checkbutton(root,variable=emoji_var)
    emoji_gui_toggle.grid(row=3,column=5,sticky=W,padx=5,pady=5)
    #

    #covert button
    convert_btn = Button(root,text="Convert", command=lambda:creatRGBIF(
        uri=input_gif_path_gui_dir_field.get(),
        operation=operator_var.get(),
        min_frames=int(minimum_frames_gui_input_field.get()),
        intensity=float(intensity_gui_input_field.get()),
        emoji=emoji_var.get(),
        output_path=output_gif_path_gui_dir_field.get()
        ))
    convert_btn.grid(row=4, column=0,columnspan=1, sticky=W,padx=5, pady=5)

    root.mainloop()
