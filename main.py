import os
import json
from tkinter import *
from MainWindow import MainWindow


def main():
    root = Tk()
    MainWindow(root)
    root.mainloop()
    # print("Starting...")
    # img_dir= 'C:/Users/William/Documents/C3P0 datasets/greenscreen/resized/'   # Image directory
    # current_img = "IMG_20210924_150708.jpg"
    #
    # root = Tk()                                                                # Create a Tkinter window
    # w, h = root.winfo_screenwidth(), root.winfo_screenheight()                 # set window size to full screen
    # root.geometry("%dx%d+0+0" % (w, h))                                        # set window size to full screen
    # root.title("C3P0")                                                         # set window title
    #
    # canvas = Canvas(root, width=1000, height=1000)                             # create canvas
    # canvas.place(x=w / 3.5, y=h / 8)                                           # place canvas
    #
    # btns = ButtonHandler(img_dir, canvas)                                              # create button handler
    #
    # img = ImageTk.PhotoImage(Image.open(f'{img_dir}{current_img}'))                # Open image
    # canvas.create_image(0, 0, anchor=NW, image=img)                            # place image on canvas
    #
    # canvas.bind("<Key>", print_pos)                                            # bind key press to print position
    # canvas.bind("<Button-1>", print_pos)                                       # bind mouse click to print position
    #
    # make_buttons(root, btns, h, w, canvas)                                     # make buttons
    # canvas.itemconfig(img, image=f'{img_dir}IMG_20210924_150717_BURST002.jpg')
    #
    # root.mainloop()                                                            # start main loop


if __name__ == "__main__":
    main()
