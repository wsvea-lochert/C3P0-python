import os
from tkinter import *
from PIL import ImageTk, Image


class ButtonHandler:
    def __init__(self, img_path, canvas):
        self.selected_joint = ""
        self.index = 0
        self.joints = ["right_wrist", "left_wrist", "right_elbow", "left_elbow", "right_shoulder", "left_shoulder",
                       "right_hip", "left_hip", "right_knee", "left_knee", "right_ankle", "left_ankle", "neck", "head",
                       "torso"]
        self.images = os.listdir(img_path)
        self.img_path = img_path


    def right_wrist(self):
        print("Right Writs selected")
        self.selected_joint = "right_wrist"
        self.index = 0
        print(self.selected_joint)

    def left_wrist(self):
        print("Left Writs selected")
        self.index = 1
        self.selected_joint = "left_wrist"

    def right_elbow(self):
        print("Right Elbow selected")
        self.index = 2
        self.selected_joint = "right_elbow"

    def left_elbow(self):
        print("Left Elbow selected")
        self.index = 3
        self.selected_joint = "left_elbow"

    def right_shoulder(self):
        print("Right Shoulder selected")
        self.index = 4
        self.selected_joint = "right_shoulder"

    def left_shoulder(self):
        print("Left Shoulder selected")
        self.index = 5
        self.selected_joint = "left_shoulder"

    def right_hip(self):
        print("Right Hip selected")
        self.index = 6
        self.selected_joint = "right_hip"

    def left_hip(self):
        print("Left Hip selected")
        self.index = 7
        self.selected_joint = "left_hip"

    def right_knee(self):
        print("Right Knee selected")
        self.index = 8
        self.selected_joint = "right_knee"

    def left_knee(self):
        print("Left Knee selected")
        self.index = 9
        self.selected_joint = "left_knee"

    def right_ankle(self):
        print("Right Ankle selected")
        self.index = 10
        self.selected_joint = "right_ankle"

    def left_ankle(self):
        print("Left Ankle selected")
        self.index = 11
        self.selected_joint = "left_ankle"

    def neck(self):
        print("Neck selected")
        self.index = 12
        self.selected_joint = "neck"

    def head(self):
        print("Head selected")
        self.index = 13
        self.selected_joint = "head"

    def torso(self):
        print("Torso selected")
        self.index = 14
        self.selected_joint = "torso"

    def save_data(self):
        print("Save data selected")

    def next_data(self, canvas):
        self.index = self.index + 1
        # canvas.create_image(0, 0, image=ImageTk.PhotoImage(Image.open(f'{self.img_path}{self.images[self.index]}')), anchor=NW)
        canvas.itemconfig(image=ImageTk.PhotoImage(Image.open(f'{self.img_path}{self.images[self.index]}')), tagOrId="img")
        # canvas.update()
        print(f"Next data selected, current image {self.images[self.index]}")

    def prev_data(self, canvas):
        if self.index != 0:
            self.index = self.index - 1
            # canvas.create_image(0, 0, image=ImageTk.PhotoImage(Image.open(f'{self.img_path}{self.images[self.index]}')), anchor=NW)
            canvas.itemconfig(image=ImageTk.PhotoImage(Image.open(f'{self.img_path}{self.images[self.index]}')),
                              tagOrId="img")
            print(f"previous data selected, current image {self.images[self.index]}")
        else:
            print("No previous data")

