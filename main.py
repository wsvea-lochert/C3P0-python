import os
import sys
import time
import json
from PIL import ImageTk, Image

from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Checkbutton, Canvas, messagebox, filedialog, ttk



def main():
    print("Starting...")
    """Open a gui window"""


    """open a gui window"""
    root = Tk()
    root.title("My GUI")
    # root.geometry("1920x1200")
    root.resizable(0, 0)
    root.configure(background="white")
    root.configure(highlightbackground="black")
    root.configure(highlightcolor="black")
    root.configure(width=1920)
    root.configure(height=1200)
    root.configure(relief="groove")

    # add a canvas
    canvas = Canvas(root, width=1000, height=1000)
    canvas.grid(row=2, column=3)

    """add an image in  to C:/Users/William/Documents/C3P0 datasets/greenscreen2/IMG_20211102_203858_BURST098.jpg the window"""
    fp = open("C:/Users/William/Documents/C3P0 datasets/greenscreen2/IMG_20211102_203858_BURST098.jpg", "rb")
    img = Image.open(fp)
    img = ImageTk.PhotoImage(img)
    l = Label(image=img)
    l.pack()
    # canvas.create_image(1000, 1000, image=img, anchor=NW)

    """open a gui window"""
    root.mainloop()



if __name__ == "__main__":
    main()