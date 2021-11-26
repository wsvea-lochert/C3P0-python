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
        root.configure(background='#3A3A3A')

        # self.make_buttons(root)                                        # Make the joint buttons

        self.img_dir = 'C:/Users/William/Documents/C3P0 datasets/greenscreen/resized/'              # Set the directory for the images
        self.images = os.listdir(self.img_dir)                                                      # Get the list of images in the directory
        self.index = 0                                                                              # Set the index to 0

        self.image_names = []                                                                       # Create a list to hold the image names
        self.photoImages = []
        self.load_images()                                                                         # Load the images

        self.canvas = Canvas(root, width=1000, height=1000)                                         # create canvas
        self.canvas.place(x=self.w / 3.5, y=self.h / 8)                                             # place canvas
        self.initial_image = self.photoImages[0]
        self.canvas_image = self.initial_image   # The initial image on the canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.canvas_image)   # place image on canvas

        self.canvas.bind("<Key>", print_pos)                                                        # bind key press to print position
        self.canvas.bind("<Button-1>", print_pos)                                                   # bind mouse click to print position

        # TODO: Button section
        self.next_button = Button(root, text="Next", command=self.next_data, height=3, width=20, bg="#11EA9B", fg="black")
        self.next_button.place(x=self.w / 2, y=self.h / 50)

        self.prev_button = Button(root, text="Prev", command=self.prev_data, height=3, width=20, bg="#EAC611", fg="black")
        self.prev_button.place(x=self.w / 2.5, y=self.h / 50)

        #  All the data points needed for our dataset.
        self.head = {'x': 0, 'y': 0}            # 0
        self.image = self.images[self.index]    # Current Image name
        self.left_ankle = {'x': 0, 'y': 0}      # 1
        self.left_elbow = {'x': 0, 'y': 0}      # 2
        self.left_hip = {'x': 0, 'y': 0}        # 3
        self.left_knee = {'x': 0, 'y': 0}       # 4
        self.left_shoulder = {'x': 0, 'y': 0}   # 5
        self.left_wrist = {'x': 0, 'y': 0}      # 6
        self.neck = {'x': 0, 'y': 0}            # 7
        self.right_ankle = {'x': 0, 'y': 0}     # 8
        self.right_elbow = {'x': 0, 'y': 0}     # 9
        self.right_hip = {'x': 0, 'y': 0}       # 10
        self.right_knee = {'x': 0, 'y': 0}      # 11
        self.right_shoulder = {'x': 0, 'y': 0}  # 12
        self.right_wrist = {'x': 0, 'y': 0}     # 13
        self.torso = {'x': 0, 'y': 0}           # 14

        self.selected_joint = 0                 # The current selected joint, change the number between 0 and 14 to change the selected joint.

        self.head_button = Button(root, text="Head", command=self.head_selected, height=2, width=20, bg='#B63DC7', fg='white')
        self.head_button.place(x=self.w / 2.5, y=self.h / 13)
        self.left_ankle_button = Button(root, text="Left Ankle", command=self.left_ankle_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_ankle_button.place(x=self.w / 5.4, y=self.h / 1.7)
        self.left_elbow_button = Button(root, text="Left Elbow", command=self.left_elbow_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_elbow_button.place(x=self.w / 5.4, y=self.h / 3.5)
        self.left_hip_button = Button(root, text="Left Hip", command=self.left_hip_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_hip_button.place(x=self.w / 5.4, y=self.h / 2.5)
        self.left_knee_button = Button(root, text="Left Knee", command=self.left_knee_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_knee_button.place(x=self.w / 5.4, y=self.h / 2)
        self.left_shoulder_button = Button(root, text="Left Shoulder", command=self.left_shoulder_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_shoulder_button.place(x=self.w / 5.4, y=self.h / 5)
        self.left_writs_button = Button(root, text="Left Writs", command=self.left_wrist_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_writs_button.place(x=self.w / 5.4, y=self.h / 3)
        self.neck_button = Button(root, text="Neck", command=self.neck_selected, height=2, width=20, bg='#B63DC7', fg='white')
        self.neck_button.place(x=self.w / 2, y=self.h / 13)
        self.right_ankle_button = Button(root, text="Right Ankle", command=self.right_ankle_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_ankle_button.place(x=self.w / 1.4, y=self.h / 1.7)
        self.right_elbow_button = Button(root, text="Right Elbow", command=self.right_elbow_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_elbow_button.place(x=self.w / 1.4, y=self.h / 3.5)
        self.right_hip_button = Button(root, text="Right Hip", command=self.right_hip_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_hip_button.place(x=self.w / 1.4, y=self.h / 2.5)
        self.right_knee_button = Button(root, text="Right Knee", command=self.right_knee_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_knee_button.place(x=self.w / 1.4, y=self.h / 2)
        self.right_shoulder_button = Button(root, text="Right Shoulder", command=self.right_shoulder_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_shoulder_button.place(x=self.w / 1.4, y=self.h / 5)
        self.right_writs_button = Button(root, text="Right Writs", command=self.right_wrist_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_writs_button.place(x=self.w / 1.4, y=self.h / 3)
        self.torso_button = Button(root, text="Torso", command=self.torso_selected, height=2, width=20, bg='#B63DC7', fg='white')
        self.torso_button.place(x=self.w / 2.2, y=self.h / 1.2)

        self.save_button = Button(root, text="Save", command=self.save_pose, height=3, width=20, bg="green", fg="white")
        self.save_button.place(x=self.w / 1.4, y=self.h / 1.3)

        """Keyboard listener if the s key is pressed run save_data()"""
        root.bind('<Key>', self.key_pressed)
        #self.canvas.bind('<s>', self.save_pose)

        self.joint_names = ['head', 'left_ankle', 'left_elbow', 'left_hip', 'left_knee', 'left_shoulder', 'left_wrist', 'neck',
                            'right_ankle', 'right_elbow', 'right_hip', 'right_knee', 'right_shoulder', 'right_wrist', 'torso']

        """Text with the currently selected joint"""
        self.selected_joint_text = Label(root, text="Selected Joint: " + self.joint_names[self.selected_joint], font=("Helvetica", 16), bg='#B63DC7', fg='white')
        self.selected_joint_text.place(x=200, y=100)

    def update_joint_text(self):
        """Updates the currently selected joint text"""
        if self.joint_names[self.selected_joint].__contains__("left"):
            self.selected_joint_text.config(text="Selected Joint: " + self.joint_names[self.selected_joint], bg='#3D84C7')
        elif self.joint_names[self.selected_joint].__contains__("right"):
            self.selected_joint_text.config(text="Selected Joint: " + self.joint_names[self.selected_joint], bg='#C7463D')
        else:
            self.selected_joint_text.config(text="Selected Joint: " + self.joint_names[self.selected_joint], bg='#B63DC7')


    def next_data(self):
        if self.index == self.images.__len__() - 1:
            print('this is the last image')
        else:
            print("Next pressed")
            self.index += 1
            self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])
            self.update_on_next()

    def prev_data(self):
        if self.index == 0:
            print('This is the first image')
        else:
            print("Prev pressed")
            self.index -= 1
            self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])

    def load_images(self):
        for image in self.images:
            self.photoImages.append(ImageTk.PhotoImage(Image.open(f'{self.img_dir}{image}').rotate(-90)))  # Remove rotate if images are not rotated when loading.

    def update_on_next(self):
        self.image = self.images[self.index]
        self.head = {'x': 0, 'y': 0}
        self.left_ankle = {'x': 0, 'y': 0}
        self.left_elbow = {'x': 0, 'y': 0}
        self.left_hip = {'x': 0, 'y': 0}
        self.left_knee = {'x': 0, 'y': 0}
        self.left_shoulder = {'x': 0, 'y': 0}
        self.left_wrist = {'x': 0, 'y': 0}
        self.neck = {'x': 0, 'y': 0}
        self.right_ankle = {'x': 0, 'y': 0}
        self.right_elbow = {'x': 0, 'y': 0}
        self.right_hip = {'x': 0, 'y': 0}
        self.right_knee = {'x': 0, 'y': 0}
        self.right_shoulder = {'x': 0, 'y': 0}
        self.right_wrist = {'x': 0, 'y': 0}
        self.torso = {'x': 0, 'y': 0}
        print(f'Next image was selected, joints updated, current image is {self.image}')

    def update_on_previous(self):
        self.image = self.images[self.index]
        print(f'Previous image was selected, joints updated, current image is {self.image}')

    def save_pose(self):
        self.head = {'x': 0, 'y': 0}
        print("Save data selected")

    def key_pressed(self, event):
        print(f"Key pressed: {event.char}")
        if event.char == 's':
            self.save_pose()
        elif event.char == 'e':
            self.next_data()
        elif event.char == 'q':
            self.prev_data()

    def head_selected(self):
        print("Head selected")
        self.selected_joint = 0
        self.update_joint_text()

    def right_wrist_selected(self):
        print("Right Writs selected")
        self.selected_joint = 13
        self.update_joint_text()

    def left_wrist_selected(self):
        print("Left Writs selected")
        self.selected_joint = 6
        self.update_joint_text()

    def right_elbow_selected(self):
        print("Right Elbow selected")
        self.selected_joint = 9
        self.update_joint_text()

    def left_elbow_selected(self):
        print("Left Elbow selected")
        self.selected_joint = 2
        self.update_joint_text()

    def right_shoulder_selected(self):
        print("Right Shoulder selected")
        self.selected_joint = 12
        self.update_joint_text()

    def left_shoulder_selected(self):
        print("Left Shoulder selected")
        self.selected_joint = 5
        self.update_joint_text()

    def right_hip_selected(self):
        print("Right Hip selected")
        self.selected_joint = 10
        self.update_joint_text()

    def left_hip_selected(self):
        print("Left Hip selected")
        self.selected_joint = 3
        self.update_joint_text()

    def right_knee_selected(self):
        print("Right Knee selected")
        self.selected_joint = 11
        self.update_joint_text()

    def left_knee_selected(self):
        print("Left Knee selected")
        self.selected_joint = 4
        self.update_joint_text()

    def right_ankle_selected(self):
        print("Right Ankle selected")
        self.selected_joint = 8
        self.update_joint_text()

    def left_ankle_selected(self):
        print("Left Ankle selected")
        self.selected_joint = 1
        self.update_joint_text()

    def neck_selected(self):
        print("Neck selected")
        self.selected_joint = 7
        self.update_joint_text()

    def torso_selected(self):
        print("Torso selected")
        self.selected_joint = 14
        self.update_joint_text()



