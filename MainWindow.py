import os
import json
from tkinter import *
from PIL import ImageTk, Image
from utils.image_handler import print_pos


class MainWindow:
    def __init__(self, root):
        print("Starting C3P0...")
        root.title("C3P0")
        self.w, self.h = root.winfo_screenwidth(), root.winfo_screenheight()  # set window size to full screen
        root.geometry("%dx%d+0+0" % (self.w, self.h))  # set window size to full screen
        root.resizable(width=True, height=True)
        root.configure(background='#ffffff')

        self.make_buttons(root)                                        # Make the joint buttons

        self.img_dir = 'C:/Users/William/Documents/C3P0 datasets/greenscreen/resized/'              # Set the directory for the images
        self.initial_image = "IMG_20210924_150708.jpg"                                              # Set the initial image to canvas
        self.images = os.listdir(self.img_dir)                                                      # Get the list of images in the directory
        self.index = 0                                                                              # Set the index to 0

        self.photoImages = []
        self.load_images()                                                                         # Load the images

        self.canvas = Canvas(root, width=1000, height=1000)                                         # create canvas
        self.canvas.place(x=self.w / 3.5, y=self.h / 8)                                             # place canvas
        self.canvas_image = ImageTk.PhotoImage(Image.open(f'{self.img_dir}{self.initial_image}'))   # The initial image on the canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.canvas_image)   # place image on canvas

        self.canvas.bind("<Key>", print_pos)                                                        # bind key press to print position
        self.canvas.bind("<Button-1>", print_pos)                                                   # bind mouse click to print position

        # TODO: Button section
        self.next_button = Button(root, text="Next", command=self.next_data, height=3, width=20, bg="#11EA9B", fg="black")
        self.next_button.place(x=self.w / 2, y=self.h / 50)

        self.prev_button = Button(root, text="Prev", command=self.prev_data, height=3, width=20, bg="#EAC611", fg="black")
        self.prev_button.place(x=self.w / 2.5, y=self.h / 50)

    def next_data(self):
        if self.index == self.images.__len__() - 1:
            print('this is the last image')
        else:
            print("Next pressed")
            self.index += 1
            self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])

    def prev_data(self):
        if self.index == 0:
            print('This is the first image')
        else:
            print("Prev pressed")
            self.index -= 1
            self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])

    def load_images(self):
        for image in self.images:
            self.photoImages.append(ImageTk.PhotoImage(Image.open(f'{self.img_dir}{image}')))



    def make_buttons(self, root):
        right_writs_button = Button(root, text="Right Writs", command=self.right_wrist, height=2, width=20, bg="#C7463D", fg='white')
        right_writs_button.place(x=self.w / 1.4, y=self.h / 3)

        right_elbow_button = Button(root, text="Right Elbow", command=self.right_elbow, height=2, width=20, bg="#C7463D", fg='white')
        right_elbow_button.place(x=self.w / 1.4, y=self.h / 3.5)

        right_shoulder_button = Button(root, text="Right Shoulder", command=self.right_shoulder, height=2, width=20,
                                       bg="#C7463D", fg='white')
        right_shoulder_button.place(x=self.w / 1.4, y=self.h / 5)

        right_hip_button = Button(root, text="Right Hip", command=self.right_hip, height=2, width=20, bg="#C7463D",
                                  fg='white')
        right_hip_button.place(x=self.w / 1.4, y=self.h / 2.5)

        right_knee_button = Button(root, text="Right Knee", command=self.right_knee, height=2, width=20, bg="#C7463D",
                                   fg='white')
        right_knee_button.place(x=self.w / 1.4, y=self.h / 2)

        right_ankle_button = Button(root, text="Right Ankle", command=self.right_ankle, height=2, width=20,
                                    bg="#C7463D", fg='white')
        right_ankle_button.place(x=self.w / 1.4, y=self.h / 1.7)

        left_writs_button = Button(root, text="Left Writs", command=self.left_wrist, height=2, width=20, bg='#3D84C7',
                                   fg='white')
        left_writs_button.place(x=self.w / 5.4, y=self.h / 3)

        left_elbow_button = Button(root, text="Left Elbow", command=self.left_elbow, height=2, width=20, bg='#3D84C7',
                                   fg='white')
        left_elbow_button.place(x=self.w / 5.4, y=self.h / 3.5)

        left_shoulder_button = Button(root, text="Left Shoulder", command=self.left_shoulder, height=2, width=20,
                                      bg='#3D84C7', fg='white')
        left_shoulder_button.place(x=self.w / 5.4, y=self.h / 5)

        left_hip_button = Button(root, text="Left Hip", command=self.left_hip, height=2, width=20, bg='#3D84C7',
                                 fg='white')
        left_hip_button.place(x=self.w / 5.4, y=self.h / 2.5)

        left_knee_button = Button(root, text="Left Knee", command=self.left_knee, height=2, width=20, bg='#3D84C7',
                                  fg='white')
        left_knee_button.place(x=self.w / 5.4, y=self.h / 2)

        left_ankle_button = Button(root, text="Left Ankle", command=self.left_ankle, height=2, width=20, bg='#3D84C7',
                                   fg='white')
        left_ankle_button.place(x=self.w / 5.4, y=self.h / 1.7)

        torso_button = Button(root, text="Torso", command=self.torso, height=2, width=20, bg='#B63DC7', fg='white')
        torso_button.place(x=self.w / 2.2, y=self.h / 1.2)

        head_button = Button(root, text="Head", command=self.head, height=2, width=20, bg='#B63DC7', fg='white')
        head_button.place(x=self.w / 2.5, y=self.h / 13)

        neck_button = Button(root, text="Neck", command=self.neck, height=2, width=20, bg='#B63DC7', fg='white')
        neck_button.place(x=self.w / 2, y=self.h / 13)

        save_button = Button(root, text="Save", command=self.save_data, height=3, width=20, bg="green", fg="white")
        save_button.place(x=self.w / 1.4, y=self.h / 1.3)

        # Buttons for handling moving through the data




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

    # def next_data(self, canvas):
    #     self.index = self.index + 1
    #     # canvas.create_image(0, 0, image=ImageTk.PhotoImage(Image.open(f'{self.img_path}{self.images[self.index]}')), anchor=NW)
    #     canvas.itemconfig(image=ImageTk.PhotoImage(Image.open(f'{self.img_path}{self.images[self.index]}')), tagOrId="img")
    #     # canvas.update()
    #     print(f"Next data selected, current image {self.images[self.index]}")
