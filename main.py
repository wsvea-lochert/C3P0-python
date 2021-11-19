import os
import sys
import time
import json
from tkinter import *
from PIL import ImageTk,Image
from utils.image_handler import print_pos
from utils.button_handler import ButtonHandler
from utils.button_maker import make_buttons


def main():
    print("Starting...")
    root = Tk()
    # set root window size
    root.geometry("1920x1200")
    btns = ButtonHandler()
    # Canvas code
    canvas = Canvas(root, width=1000, height=1000)
    # set canvas background to black
    canvas.configure(background='black')
    canvas.pack()
    img = ImageTk.PhotoImage(Image.open("C:/Users/William/Documents/C3P0 datasets/greenscreen/resized/IMG_20210924_150708.jpg"))
    canvas.create_image(0, 0, anchor=NW, image=img)

    canvas.bind("<Key>", print_pos)
    canvas.bind("<Button-1>", print_pos)

    make_buttons(root, btns)
    
    root.mainloop()

    """open a gui window"""
    root.mainloop()



if __name__ == "__main__":
    main()