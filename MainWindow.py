import os
import json
from tkinter import *
from PIL import ImageTk, Image
from predict_pose import predict_pose, predict_pose_movenet
import numpy as np


class MainWindow:
    def __init__(self, root):
        print("Starting C3P0...")
        root.title("C3P0")
        self.w, self.h = root.winfo_screenwidth(), root.winfo_screenheight()  # set window size to full screen
        root.geometry("%dx%d+0+0" % (self.w, self.h))  # set window size to full screen
        root.resizable(width=True, height=True)
        root.configure(background='#3A3A3A')

        self.img_dir = 'resized_img/'                  # Set the directory for the images
        self.images = os.listdir(self.img_dir)                                                      # Get the list of images in the directory
        # sort self.images
        self.images.sort()
        self.index = 0                                                                              # Set the index to 0

        self.json_dir = 'dataset3.json'                                                             # Set the directory for the json file
        self.json_dict = {}                                                                         # Create a dictionary to store the json data
        self.json_pose = {}
        self.get_json()                                                                             # Get the json data

        self.image_names = []                                                                       # Create a list to hold the image names
        self.photoImages = []                                                                       # Create a list to hold the photo images
        self.load_images()                                                                          # Load the images

        self.canvas = Canvas(root, width=1000, height=1000)                                         # create canvas
        self.canvas.place(x=self.w / 3.5, y=self.h / 8)                                             # place canvas
        self.initial_image = self.photoImages[self.index]                                           # set initial image
        self.canvas_image = self.initial_image                                                      # The initial image on the canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.canvas_image)   # place image on canvas

        self.canvas.bind("<Key>", self.print_pos)                                                        # bind key press to print position
        self.canvas.bind("<Button-1>", self.print_pos)                                                   # bind mouse click to print position

        # Button section
        self.next_button = Button(root, text="Next", command=self.next_data, height=3, width=20, bg="#11EA9B", fg="black")
        self.next_button.place(x=self.w / 2, y=self.h / 50)

        self.prev_button = Button(root, text="Prev", command=self.prev_data, height=3, width=20, bg="#EAC611", fg="black")
        self.prev_button.place(x=self.w / 2.5, y=self.h / 50)

        self.zero_out = Button(root, text="Zero current", command=self.zero_current, height=3, width=20, bg="#EAC611", fg="black")
        self.zero_out.place(x=self.w / 3.4, y=self.h / 50)

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
        self.left_angle = 0                    # The angle between the selected joint and the left elbow
        self.right_angle = 0                   # The angle between the selected joint and the right elbow

        # coordinates used to draw a ruler for angles in hips and shoulders.
        self.rp1 = {'x': 0, 'y': 0}
        self.rp2 = {'x': 0, 'y': 0}
        # TODO: Draw a line between RP1 and RP2 on canvas
        """ 
        1. Draw a line between rp1 and rp2 if they are not 0,0 & 0,0.
        2. If either of the points are in 0,0 do NOT draw them.
        3. Only drawable when they are selected with buttons or adjusted with specific buttons.
        4. Add a zero function for both points with one click.
        5. 
        """
        # TODO: implement posenet for assisting in labeling?

        # More buttons.
        self.head_button = Button(root, text=f"Head x: {self.head['x']} y:{self.head['y']}", command=self.head_selected, height=2, width=20, bg='#B63DC7', fg='white')
        self.head_button.place(x=self.w / 2.5, y=self.h / 13)
        self.left_ankle_button = Button(root, text=f"Left Ankle x: {self.left_ankle['x']} y: {self.left_ankle['y']}", command=self.left_ankle_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_ankle_button.place(x=self.w / 5.4, y=self.h / 1.7)
        self.left_elbow_button = Button(root, text=f"Left Elbow x: {self.left_elbow['x']} y: {self.left_elbow['y']}", command=self.left_elbow_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_elbow_button.place(x=self.w / 5.4, y=self.h / 3.5)
        self.left_hip_button = Button(root, text=f"Left Hip x: {self.left_hip['x']} y: {self.left_hip['y']}", command=self.left_hip_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_hip_button.place(x=self.w / 5.4, y=self.h / 2.5)
        self.left_knee_button = Button(root, text=f"Left Knee x: {self.left_knee['x']} y: {self.left_knee['y']}", command=self.left_knee_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_knee_button.place(x=self.w / 5.4, y=self.h / 2)
        self.left_shoulder_button = Button(root, text=f"Left Shoulder x: {self.left_shoulder['x']} y: {self.left_shoulder['y']}", command=self.left_shoulder_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_shoulder_button.place(x=self.w / 5.4, y=self.h / 5)
        self.left_writs_button = Button(root, text=f"Left Writs x: {self.left_wrist['x']} y: {self.left_wrist['y']}", command=self.left_wrist_selected, height=2, width=20, bg='#3D84C7', fg='white')
        self.left_writs_button.place(x=self.w / 5.4, y=self.h / 3)
        self.neck_button = Button(root, text=f"Neck x: {self.neck['x']} y: {self.neck['y']}", command=self.neck_selected, height=2, width=20, bg='#B63DC7', fg='white')
        self.neck_button.place(x=self.w / 2, y=self.h / 13)
        self.right_ankle_button = Button(root, text=f"Right Ankle x: {self.right_ankle['x']} y: {self.right_ankle['y']}", command=self.right_ankle_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_ankle_button.place(x=self.w / 1.3, y=self.h / 1.7)
        self.right_elbow_button = Button(root, text=f"Right Elbow x: {self.right_elbow['x']} y: {self.right_elbow['y']}", command=self.right_elbow_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_elbow_button.place(x=self.w / 1.3, y=self.h / 3.5)
        self.right_hip_button = Button(root, text=f"Right Hip x: {self.right_hip['x']} y: {self.right_hip['y']}", command=self.right_hip_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_hip_button.place(x=self.w / 1.3, y=self.h / 2.5)
        self.right_knee_button = Button(root, text=f"Right Knee x: {self.right_knee['x']} y: {self.right_knee['y']}", command=self.right_knee_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_knee_button.place(x=self.w / 1.3, y=self.h / 2)
        self.right_shoulder_button = Button(root, text=f"Right Shoulder x: {self.right_shoulder['x']} y: {self.right_shoulder['y']}", command=self.right_shoulder_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_shoulder_button.place(x=self.w / 1.3, y=self.h / 5)
        self.right_writs_button = Button(root, text=f"Right Writs x: {self.right_wrist['x']} y: {self.right_wrist['y']}", command=self.right_wrist_selected, height=2, width=20, bg="#C7463D", fg='white')
        self.right_writs_button.place(x=self.w / 1.3, y=self.h / 3)
        self.torso_button = Button(root, text=f"Torso x: {self.torso['x']} y: {self.torso['y']}", command=self.torso_selected, height=2, width=20, bg='#B63DC7', fg='white')
        self.torso_button.place(x=self.w / 2.2, y=self.h / 1.2)

        self.save_button = Button(root, text="Save", command=self.save_pose, height=3, width=20, bg="green", fg="white")
        self.save_button.place(x=self.w / 1.3, y=self.h / 1.3)

        self.rotate_image_button = Button(root, text="Rotate image", command=self.rotate_image, height=3, width=20, bg="black", fg="white")
        self.rotate_image_button.place(x=self.w / 1.1, y=self.h / 1.3)

        self.prev_pose_button = Button(root, text="Get prev pose", command=self.get_previous_pose, height=3, width=20,
                                          bg="white", fg="black")
        self.prev_pose_button.place(x=self.w / 1.1, y=self.h / 1.4)

        self.update_joints_from_json()
        """draw a circle on self.canvas"""
        self.head_circle = self.canvas.create_arc(self.head['x'] - 5, self.head['y'] - 5, self.head['x'] + 5, self.head['y'] + 5, start=0, extent=359, fill='#B63DC7')
        self.left_ankle_circle = self.canvas.create_arc(self.left_ankle['x'] - 5, self.left_ankle['y'] - 5, self.left_ankle['x'] + 5, self.left_ankle['y'] + 5, start=0, extent=359, fill='#3D84C7')
        self.left_elbow_circle = self.canvas.create_arc(self.left_elbow['x'] - 5, self.left_elbow['y'] - 5, self.left_elbow['x'] + 5, self.left_elbow['y'] + 5, start=0, extent=359, fill='#3D84C7')
        self.left_hip_circle = self.canvas.create_arc(self.left_hip['x'] - 5, self.left_hip['y'] - 5, self.left_hip['x'] + 5, self.left_hip['y'] + 5, start=0, extent=359, fill='#3D84C7')
        self.left_knee_circle = self.canvas.create_arc(self.left_knee['x'] - 5, self.left_knee['y'] - 5, self.left_knee['x'] + 5, self.left_knee['y'] + 5, start=0, extent=359, fill='#3D84C7')
        self.left_shoulder_circle = self.canvas.create_arc(self.left_shoulder['x'] - 5, self.left_shoulder['y'] - 5, self.left_shoulder['x'] + 5, self.left_shoulder['y'] + 5, start=0, extent=359, fill='#3D84C7')
        self.left_wrist_circle = self.canvas.create_arc(self.left_wrist['x'] - 5, self.left_wrist['y'] - 5, self.left_wrist['x'] + 5, self.left_wrist['y'] + 5, start=0, extent=359, fill='#3D84C7')
        self.neck_circle = self.canvas.create_arc(self.neck['x'] - 5, self.neck['y'] - 5, self.neck['x'] + 5, self.neck['y'] + 5, start=0, extent=359, fill='#B63DC7')
        self.right_ankle_circle = self.canvas.create_arc(self.right_ankle['x'] - 5, self.right_ankle['y'] - 5, self.right_ankle['x'] + 5, self.right_ankle['y'] + 5, start=0, extent=359, fill='#C7463D')
        self.right_elbow_circle = self.canvas.create_arc(self.right_elbow['x'] - 5, self.right_elbow['y'] - 5, self.right_elbow['x'] + 5, self.right_elbow['y'] + 5, start=0, extent=359, fill='#C7463D')
        self.right_hip_circle = self.canvas.create_arc(self.right_hip['x'] - 5, self.right_hip['y'] - 5, self.right_hip['x'] + 5, self.right_hip['y'] + 5, start=0, extent=359, fill='#C7463D')
        self.right_knee_circle = self.canvas.create_arc(self.right_knee['x'] - 5, self.right_knee['y'] - 5, self.right_knee['x'] + 5, self.right_knee['y'] + 5, start=0, extent=359, fill='#C7463D')
        self.right_shoulder_circle = self.canvas.create_arc(self.right_shoulder['x'] - 5, self.right_shoulder['y'] - 5, self.right_shoulder['x'] + 5, self.right_shoulder['y'] + 5, start=0, extent=359, fill='#C7463D')
        self.right_wrist_circle = self.canvas.create_arc(self.right_wrist['x'] - 5, self.right_wrist['y'] - 5, self.right_wrist['x'] + 5, self.right_wrist['y'] + 5, start=0, extent=359, fill='#C7463D')
        self.torso_circle = self.canvas.create_arc(self.torso['x'] - 5, self.torso['y'] - 5, self.torso['x'] + 5, self.torso['y'] + 5, start=0, extent=359, fill='#B63DC7')

        """Keyboard listener if the s key is pressed run save_data()"""
        root.bind('<Key>', self.key_pressed)
        #self.canvas.bind('<s>', self.save_pose)

        self.joint_names = ['head', 'left_ankle', 'left_elbow', 'left_hip', 'left_knee', 'left_shoulder', 'left_wrist', 'neck',
                            'right_ankle', 'right_elbow', 'right_hip', 'right_knee', 'right_shoulder', 'right_writs', 'torso']

        """Text with the currently selected joint"""
        self.selected_joint_text = Label(root, text="Selected Joint: " + self.joint_names[self.selected_joint], font=("Helvetica", 16), bg='#B63DC7', fg='white')
        self.selected_joint_text.place(x=200, y=100)

        self.index_text = Label(root, text=f"Current index {self.index} / {self.images.__len__()}", font=("Helvetica", 16), bg='#B63DC7', fg='white')
        self.index_text.place(x=200, y=200)

        self.left_arm_angle_text = Label(root, text="Left arm angle: " + str(self.left_angle),
                                         font=("Helvetica", 16), bg='#B63DC7', fg='white')
        self.left_arm_angle_text.place(x=200, y=300)

        self.right_arm_angle_text = Label(root, text="Left arm angle: " + str(self.right_angle),
                                          font=("Helvetica", 16), bg='#B63DC7', fg='white')
        self.right_arm_angle_text.place(x=200, y=400)

    def zero_current(self):
        # set the current joint to 0, 0 and update button text, circles
        if self.selected_joint == 0:
            self.head['x'] = 0
            self.head['y'] = 0
        elif self.selected_joint == 1:
            self.left_ankle['x'] = 0
            self.left_ankle['y'] = 0
        elif self.selected_joint == 2:
            self.left_elbow['x'] = 0
            self.left_elbow['y'] = 0
        elif self.selected_joint == 3:
            self.left_hip['x'] = 0
            self.left_hip['y'] = 0
        elif self.selected_joint == 4:
            self.left_knee['x'] = 0
            self.left_knee['y'] = 0
        elif self.selected_joint == 5:
            self.left_shoulder['x'] = 0
            self.left_shoulder['y'] = 0
        elif self.selected_joint == 6:
            self.left_wrist['x'] = 0
            self.left_wrist['y'] = 0
        elif self.selected_joint == 7:
            self.neck['x'] = 0
            self.neck['y'] = 0
        elif self.selected_joint == 8:
            self.right_ankle['x'] = 0
            self.right_ankle['y'] = 0
        elif self.selected_joint == 9:
            self.right_elbow['x'] = 0
            self.right_elbow['y'] = 0
        elif self.selected_joint == 10:
            self.right_hip['x'] = 0
            self.right_hip['y'] = 0
        elif self.selected_joint == 11:
            self.right_knee['x'] = 0
            self.right_knee['y'] = 0
        elif self.selected_joint == 12:
            self.right_shoulder['x'] = 0
            self.right_shoulder['y'] = 0
        elif self.selected_joint == 13:
            self.right_wrist['x'] = 0
            self.right_wrist['y'] = 0
        elif self.selected_joint == 14:
            self.torso['x'] = 0
            self.torso['y'] = 0

        self.set_button_text()
        self.update_circles()

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
            self.index_text.config(text=f'Current index: {self.index} / {self.images.__len__()}')
            self.image = self.images[self.index]
        else:
            print("Next pressed")
            self.index = self.index + 1
            self.image = self.images[self.index]
            self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])
            self.update_joints_from_json()
            self.set_button_text()
            self.update_circles()
            self.index_text.config(text=f'Current index: {self.index} / {self.images.__len__()}')
            self.get_left_angle()
            self.get_right_angle()
            self.left_arm_angle_text.config(text="Left arm angle: " + str(self.left_angle))
            self.right_arm_angle_text.config(text="Right arm angle: " + str(self.right_angle))

    def skip_hundred(self):
        if self.index == self.images.__len__() - 1:
            print('this is the last image')
            self.index_text.config(text=f'Current index: {self.index} / {self.images.__len__()}')
            self.image = self.images[self.index]
        else:
            print("Next pressed")
            self.index = self.index + 1000
            self.image = self.images[self.index]
            self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])
            self.update_joints_from_json()
            self.set_button_text()
            self.update_circles()
            self.index_text.config(text=f'Current index: {self.index} / {self.images.__len__()}')

    def prev_data(self):
        if self.index == 0:
            self.update_joints_from_json()
            self.set_button_text()
            print('This is the first image')
            self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])
            self.index_text.config(text=f'Current index: {self.index} / {self.images.__len__()}')
            self.image = self.images[self.index]
            self.get_left_angle()
            self.get_right_angle()
            self.left_arm_angle_text.config(text="Left arm angle: " + str(self.left_angle))
            self.right_arm_angle_text.config(text="Right arm angle: " + str(self.right_angle))
        else:
            print("Prev pressed")
            self.index = self.index - 1
            self.image = self.images[self.index]
            self.update_joints_from_json()
            self.set_button_text()
            self.update_circles()
            self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])
            self.index_text.config(text=f'Current index: {self.index} / {self.images.__len__()}')
            self.get_left_angle()
            self.get_right_angle()
            self.left_arm_angle_text.config(text="Left arm angle: " + str(self.left_angle))
            self.right_arm_angle_text.config(text="Right arm angle: " + str(self.right_angle))

    def load_images(self):
        for image in self.images:
            self.photoImages.append(ImageTk.PhotoImage(Image.open(f'{self.img_dir}{image}')))  # TODO Remove rotate if images are not rotated when loading.

    def update_joints_from_json(self):
        """if json file contains the current image update joints"""
        self.get_json()
        try:
            print("image found")
            self.head['x'] = self.json_dict[f'image{self.index}']['head']['x']
            self.head['y'] = self.json_dict[f'image{self.index}']['head']['y']
            self.left_ankle['x'] = self.json_dict[f'image{self.index}']['left_ankle']['x']
            self.left_ankle['y'] = self.json_dict[f'image{self.index}']['left_ankle']['y']
            self.left_elbow['x'] = self.json_dict[f'image{self.index}']['left_elbow']['x']
            self.left_elbow['y'] = self.json_dict[f'image{self.index}']['left_elbow']['y']
            self.left_hip['x'] = self.json_dict[f'image{self.index}']['left_hip']['x']
            self.left_hip['y'] = self.json_dict[f'image{self.index}']['left_hip']['y']
            self.left_knee['x'] = self.json_dict[f'image{self.index}']['left_knee']['x']
            self.left_knee['y'] = self.json_dict[f'image{self.index}']['left_knee']['y']
            self.left_shoulder['x'] = self.json_dict[f'image{self.index}']['left_shoulder']['x']
            self.left_shoulder['y'] = self.json_dict[f'image{self.index}']['left_shoulder']['y']
            self.left_wrist['x'] = self.json_dict[f'image{self.index}']['left_wrist']['x']
            self.left_wrist['y'] = self.json_dict[f'image{self.index}']['left_wrist']['y']
            self.neck['x'] = self.json_dict[f'image{self.index}']['neck']['x']
            self.neck['y'] = self.json_dict[f'image{self.index}']['neck']['y']
            self.right_ankle['x'] = self.json_dict[f'image{self.index}']['right_ankle']['x']
            self.right_ankle['y'] = self.json_dict[f'image{self.index}']['right_ankle']['y']
            self.right_elbow['x'] = self.json_dict[f'image{self.index}']['right_elbow']['x']
            self.right_elbow['y'] = self.json_dict[f'image{self.index}']['right_elbow']['y']
            self.right_hip['x'] = self.json_dict[f'image{self.index}']['right_hip']['x']
            self.right_hip['y'] = self.json_dict[f'image{self.index}']['right_hip']['y']
            self.right_knee['x'] = self.json_dict[f'image{self.index}']['right_knee']['x']
            self.right_knee['y'] = self.json_dict[f'image{self.index}']['right_knee']['y']
            self.right_shoulder['x'] = self.json_dict[f'image{self.index}']['right_shoulder']['x']
            self.right_shoulder['y'] = self.json_dict[f'image{self.index}']['right_shoulder']['y']
            self.right_wrist['x'] = self.json_dict[f'image{self.index}']['right_writs']['x']
            self.right_wrist['y'] = self.json_dict[f'image{self.index}']['right_writs']['y']
            self.torso['x'] = self.json_dict[f'image{self.index}']['torso']['x']
            self.torso['y'] = self.json_dict[f'image{self.index}']['torso']['y']
            self.set_button_text()
        except KeyError:
            print("Image not found, setting coordinates to 0,0")
            self.set_coordinates_zero()
            self.set_button_text()

    def calculate_angle(self, shoulder, elbow, wrist):
        """
            Calculates the angle between three points.
            """
        a = np.array([shoulder['x'], shoulder['y']])
        b = np.array([elbow['x'], elbow['y']])
        c = np.array([wrist['x'], wrist['y']])
        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))  # cosine of the angle
        angle = np.arccos(cosine_angle)  # angle in radians
        return np.degrees(angle)  # angle in degrees

    def get_left_angle(self):
        angle = self.calculate_angle(self.left_hip, self.left_shoulder, self.left_elbow)
        self.left_angle = angle

    def get_right_angle(self):
        angle = self.calculate_angle(self.right_hip, self.right_shoulder, self.right_elbow)
        self.right_angle = angle

    def set_coordinates_zero(self):
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

    def rotate_image(self):
        """Rotate the current image and update the canvas"""
        self.photoImages[self.index] = ImageTk.PhotoImage(Image.open(f'{self.img_dir}{self.image}').rotate(90))
        self.canvas.itemconfig(self.image_on_canvas, image=self.photoImages[self.index])
        print(f'Image rotated, current image is {self.image}')

    def set_button_text(self):
        self.head_button.config(text=f'Head x: {self.head["x"]} y: {self.head["y"]}')
        self.left_ankle_button.config(text=f'Left ankle x: {self.left_ankle["x"]} y: {self.left_ankle["y"]}')
        self.left_elbow_button.config(text=f'Left elbow x: {self.left_elbow["x"]} y: {self.left_elbow["y"]}')
        self.left_hip_button.config(text=f'Left hip x: {self.left_hip["x"]} y: {self.left_hip["y"]}')
        self.left_knee_button.config(text=f'Left knee x: {self.left_knee["x"]} y: {self.left_knee["y"]}')
        self.left_shoulder_button.config(text=f'Left shoulder x: {self.left_shoulder["x"]} y: {self.left_shoulder["y"]}')
        self.left_writs_button.config(text=f'Left wrist x: {self.left_wrist["x"]} y: {self.left_wrist["y"]}')
        self.neck_button.config(text=f'Neck x: {self.neck["x"]} y: {self.neck["y"]}')
        self.right_ankle_button.config(text=f'Right ankle x: {self.right_ankle["x"]} y: {self.right_ankle["y"]}')
        self.right_elbow_button.config(text=f'Right elbow x: {self.right_elbow["x"]} y: {self.right_elbow["y"]}')
        self.right_hip_button.config(text=f'Right hip x: {self.right_hip["x"]} y: {self.right_hip["y"]}')
        self.right_knee_button.config(text=f'Right knee x: {self.right_knee["x"]} y: {self.right_knee["y"]}')
        self.right_shoulder_button.config(text=f'Right shoulder x: {self.right_shoulder["x"]} y: {self.right_shoulder["y"]}')
        self.right_writs_button.config(text=f'Right wrist x: {self.right_wrist["x"]} y: {self.right_wrist["y"]}')
        self.torso_button.config(text=f'Torso x: {self.torso["x"]} y: {self.torso["y"]}')

    def get_next_pose(self):
        self.get_json()
        print('Getting the next pose')
        try:
            print("image found")
            self.head['x'] = self.json_dict[f'image{self.index+1}']['head']['x']
            self.head['y'] = self.json_dict[f'image{self.index+1}']['head']['y']
            self.left_ankle['x'] = self.json_dict[f'image{self.index+1}']['left_ankle']['x']
            self.left_ankle['y'] = self.json_dict[f'image{self.index+1}']['left_ankle']['y']
            self.left_elbow['x'] = self.json_dict[f'image{self.index+1}']['left_elbow']['x']
            self.left_elbow['y'] = self.json_dict[f'image{self.index+1}']['left_elbow']['y']
            self.left_hip['x'] = self.json_dict[f'image{self.index+1}']['left_hip']['x']
            self.left_hip['y'] = self.json_dict[f'image{self.index+1}']['left_hip']['y']
            self.left_knee['x'] = self.json_dict[f'image{self.index+1}']['left_knee']['x']
            self.left_knee['y'] = self.json_dict[f'image{self.index+1}']['left_knee']['y']
            self.left_shoulder['x'] = self.json_dict[f'image{self.index+1}']['left_shoulder']['x']
            self.left_shoulder['y'] = self.json_dict[f'image{self.index+1}']['left_shoulder']['y']
            self.left_wrist['x'] = self.json_dict[f'image{self.index+1}']['left_wrist']['x']
            self.left_wrist['y'] = self.json_dict[f'image{self.index+1}']['left_wrist']['y']
            self.neck['x'] = self.json_dict[f'image{self.index+1}']['neck']['x']
            self.neck['y'] = self.json_dict[f'image{self.index+1}']['neck']['y']
            self.right_ankle['x'] = self.json_dict[f'image{self.index+1}']['right_ankle']['x']
            self.right_ankle['y'] = self.json_dict[f'image{self.index+1}']['right_ankle']['y']
            self.right_elbow['x'] = self.json_dict[f'image{self.index+1}']['right_elbow']['x']
            self.right_elbow['y'] = self.json_dict[f'image{self.index+1}']['right_elbow']['y']
            self.right_hip['x'] = self.json_dict[f'image{self.index+1}']['right_hip']['x']
            self.right_hip['y'] = self.json_dict[f'image{self.index+1}']['right_hip']['y']
            self.right_knee['x'] = self.json_dict[f'image{self.index+1}']['right_knee']['x']
            self.right_knee['y'] = self.json_dict[f'image{self.index+1}']['right_knee']['y']
            self.right_shoulder['x'] = self.json_dict[f'image{self.index+1}']['right_shoulder']['x']
            self.right_shoulder['y'] = self.json_dict[f'image{self.index+1}']['right_shoulder']['y']
            self.right_wrist['x'] = self.json_dict[f'image{self.index+1}']['right_writs']['x']
            self.right_wrist['y'] = self.json_dict[f'image{self.index+1}']['right_writs']['y']
            self.torso['x'] = self.json_dict[f'image{self.index+1}']['torso']['x']
            self.torso['y'] = self.json_dict[f'image{self.index+1}']['torso']['y']
            self.set_button_text()
            self.update_circles()
        except KeyError:
            print("Image not found, setting coordinates to 0,0")
            self.set_coordinates_zero()
            self.set_button_text()
            self.update_circles()

    def get_previous_pose(self):
        self.get_json()
        print('Getting previous pose.')
        try:
            print("image found")
            self.head['x'] = self.json_dict[f'image{self.index-1}']['head']['x']
            self.head['y'] = self.json_dict[f'image{self.index-1}']['head']['y']
            self.left_ankle['x'] = self.json_dict[f'image{self.index-1}']['left_ankle']['x']
            self.left_ankle['y'] = self.json_dict[f'image{self.index-1}']['left_ankle']['y']
            self.left_elbow['x'] = self.json_dict[f'image{self.index-1}']['left_elbow']['x']
            self.left_elbow['y'] = self.json_dict[f'image{self.index-1}']['left_elbow']['y']
            self.left_hip['x'] = self.json_dict[f'image{self.index-1}']['left_hip']['x']
            self.left_hip['y'] = self.json_dict[f'image{self.index-1}']['left_hip']['y']
            self.left_knee['x'] = self.json_dict[f'image{self.index-1}']['left_knee']['x']
            self.left_knee['y'] = self.json_dict[f'image{self.index-1}']['left_knee']['y']
            self.left_shoulder['x'] = self.json_dict[f'image{self.index-1}']['left_shoulder']['x']
            self.left_shoulder['y'] = self.json_dict[f'image{self.index-1}']['left_shoulder']['y']
            self.left_wrist['x'] = self.json_dict[f'image{self.index-1}']['left_wrist']['x']
            self.left_wrist['y'] = self.json_dict[f'image{self.index-1}']['left_wrist']['y']
            self.neck['x'] = self.json_dict[f'image{self.index-1}']['neck']['x']
            self.neck['y'] = self.json_dict[f'image{self.index-1}']['neck']['y']
            self.right_ankle['x'] = self.json_dict[f'image{self.index-1}']['right_ankle']['x']
            self.right_ankle['y'] = self.json_dict[f'image{self.index-1}']['right_ankle']['y']
            self.right_elbow['x'] = self.json_dict[f'image{self.index-1}']['right_elbow']['x']
            self.right_elbow['y'] = self.json_dict[f'image{self.index-1}']['right_elbow']['y']
            self.right_hip['x'] = self.json_dict[f'image{self.index-1}']['right_hip']['x']
            self.right_hip['y'] = self.json_dict[f'image{self.index-1}']['right_hip']['y']
            self.right_knee['x'] = self.json_dict[f'image{self.index-1}']['right_knee']['x']
            self.right_knee['y'] = self.json_dict[f'image{self.index-1}']['right_knee']['y']
            self.right_shoulder['x'] = self.json_dict[f'image{self.index-1}']['right_shoulder']['x']
            self.right_shoulder['y'] = self.json_dict[f'image{self.index-1}']['right_shoulder']['y']
            self.right_wrist['x'] = self.json_dict[f'image{self.index-1}']['right_writs']['x']
            self.right_wrist['y'] = self.json_dict[f'image{self.index-1}']['right_writs']['y']
            self.torso['x'] = self.json_dict[f'image{self.index-1}']['torso']['x']
            self.torso['y'] = self.json_dict[f'image{self.index-1}']['torso']['y']
            self.set_button_text()
            self.update_circles()
        except KeyError:
            print("Image not found, setting coordinates to 0,0")
            self.set_coordinates_zero()
            self.set_button_text()

    def move_current_down(self):
        if self.selected_joint == 0:
            self.head['y'] += 1
        elif self.selected_joint == 1:
            self.left_ankle['y'] += 1
        elif self.selected_joint == 2:
            self.left_elbow['y'] += 1
        elif self.selected_joint == 3:
            self.left_hip['y'] += 1
        elif self.selected_joint == 4:
            self.left_knee['y'] += 1
        elif self.selected_joint == 5:
            self.left_shoulder['y'] += 1
        elif self.selected_joint == 6:
            self.left_wrist['y'] += 1
        elif self.selected_joint == 7:
            self.neck['y'] += 1
        elif self.selected_joint == 8:
            self.right_ankle['y'] += 1
        elif self.selected_joint == 9:
            self.right_elbow['y'] += 1
        elif self.selected_joint == 10:
            self.right_hip['y'] += 1
        elif self.selected_joint == 11:
            self.right_knee['y'] += 1
        elif self.selected_joint == 12:
            self.right_shoulder['y'] +=1
        elif self.selected_joint == 13:
            self.right_wrist['y'] += 1
        elif self.selected_joint == 14:
            self.torso['y'] += 1
        self.update_circles()
        self.set_button_text()

    def move_current_up(self):
        if self.selected_joint == 0:
            self.head['y'] -= 1
        elif self.selected_joint == 1:
            self.left_ankle['y'] -= 1
        elif self.selected_joint == 2:
            self.left_elbow['y'] -= 1
        elif self.selected_joint == 3:
            self.left_hip['y'] -= 1
        elif self.selected_joint == 4:
            self.left_knee['y'] -= 1
        elif self.selected_joint == 5:
            self.left_shoulder['y'] -= 1
        elif self.selected_joint == 6:
            self.left_wrist['y'] -= 1
        elif self.selected_joint == 7:
            self.neck['y'] -= 1
        elif self.selected_joint == 8:
            self.right_ankle['y'] -= 1
        elif self.selected_joint == 9:
            self.right_elbow['y'] -= 1
        elif self.selected_joint == 10:
            self.right_hip['y'] -= 1
        elif self.selected_joint == 11:
            self.right_knee['y'] -= 1
        elif self.selected_joint == 12:
            self.right_shoulder['y'] -= 1
        elif self.selected_joint == 13:
            self.right_wrist['y'] -= 1
        elif self.selected_joint == 14:
            self.torso['y'] -= 1
        self.update_circles()
        self.set_button_text()

    def move_current_left(self):
        if self.selected_joint == 0:
            self.head['x'] -= 1
        elif self.selected_joint == 1:
            self.left_ankle['x'] -= 1
        elif self.selected_joint == 2:
            self.left_elbow['x'] -= 1
        elif self.selected_joint == 3:
            self.left_hip['x'] -= 1
        elif self.selected_joint == 4:
            self.left_knee['x'] -= 1
        elif self.selected_joint == 5:
            self.left_shoulder['x'] -= 1
        elif self.selected_joint == 6:
            self.left_wrist['x'] -= 1
        elif self.selected_joint == 7:
            self.neck['x'] -= 1
        elif self.selected_joint == 8:
            self.right_ankle['x'] -= 1
        elif self.selected_joint == 9:
            self.right_elbow['x'] -= 1
        elif self.selected_joint == 10:
            self.right_hip['x'] -= 1
        elif self.selected_joint == 11:
            self.right_knee['x'] -= 1
        elif self.selected_joint == 12:
            self.right_shoulder['x'] -= 1
        elif self.selected_joint == 13:
            self.right_wrist['x'] -= 1
        elif self.selected_joint == 14:
            self.torso['x'] -= 1
        self.update_circles()
        self.set_button_text()

    def move_current_right(self):
        if self.selected_joint == 0:
            self.head['x'] += 1
        elif self.selected_joint == 1:
            self.left_ankle['x'] += 1
        elif self.selected_joint == 2:
            self.left_elbow['x'] += 1
        elif self.selected_joint == 3:
            self.left_hip['x'] += 1
        elif self.selected_joint == 4:
            self.left_knee['x'] += 1
        elif self.selected_joint == 5:
            self.left_shoulder['x'] += 1
        elif self.selected_joint == 6:
            self.left_wrist['x'] += 1
        elif self.selected_joint == 7:
            self.neck['x'] += 1
        elif self.selected_joint == 8:
            self.right_ankle['x'] += 1
        elif self.selected_joint == 9:
            self.right_elbow['x'] += 1
        elif self.selected_joint == 10:
            self.right_hip['x'] += 1
        elif self.selected_joint == 11:
            self.right_knee['x'] += 1
        elif self.selected_joint == 12:
            self.right_shoulder['x'] += 1
        elif self.selected_joint == 13:
            self.right_wrist['x'] += 1
        elif self.selected_joint == 14:
            self.torso['x'] += 1
        self.update_circles()
        self.set_button_text()

    def move_pose_down(self):
        self.head['y'] += 1
        self.left_ankle['y'] += 1
        self.left_elbow['y'] += 1
        self.left_hip['y'] += 1
        self.left_knee['y'] += 1
        self.left_shoulder['y'] += 1
        self.left_wrist['y'] += 1
        self.neck['y'] += 1
        self.right_ankle['y'] += 1
        self.right_elbow['y'] += 1
        self.right_hip['y'] += 1
        self.right_knee['y'] += 1
        self.right_shoulder['y'] += 1
        self.right_wrist['y'] += 1
        self.torso['y'] += 1
        self.update_circles()
        self.set_button_text()

    def move_pose_up(self):
        self.head['y'] -= 1
        self.left_ankle['y'] -= 1
        self.left_elbow['y'] -= 1
        self.left_hip['y'] -= 1
        self.left_knee['y'] -= 1
        self.left_shoulder['y'] -= 1
        self.left_wrist['y'] -= 1
        self.neck['y'] -= 1
        self.right_ankle['y'] -= 1
        self.right_elbow['y'] -= 1
        self.right_hip['y'] -= 1
        self.right_knee['y'] -= 1
        self.right_shoulder['y'] -= 1
        self.right_wrist['y'] -= 1
        self.torso['y'] -= 1
        self.update_circles()
        self.set_button_text()

    def move_pose_left(self):
        self.head['x'] -= 1
        self.left_ankle['x'] -= 1
        self.left_elbow['x'] -= 1
        self.left_hip['x'] -= 1
        self.left_knee['x'] -= 1
        self.left_shoulder['x'] -= 1
        self.left_wrist['x'] -= 1
        self.neck['x'] -= 1
        self.right_ankle['x'] -= 1
        self.right_elbow['x'] -= 1
        self.right_hip['x'] -= 1
        self.right_knee['x'] -= 1
        self.right_shoulder['x'] -= 1
        self.right_wrist['x'] -= 1
        self.torso['x'] -= 1
        self.update_circles()
        self.set_button_text()

    def move_pose_right(self):
        self.head['x'] += 1
        self.left_ankle['x'] += 1
        self.left_elbow['x'] += 1
        self.left_hip['x'] += 1
        self.left_knee['x'] += 1
        self.left_shoulder['x'] += 1
        self.left_wrist['x'] += 1
        self.neck['x'] += 1
        self.right_ankle['x'] += 1
        self.right_elbow['x'] += 1
        self.right_hip['x'] += 1
        self.right_knee['x'] += 1
        self.right_shoulder['x'] += 1
        self.right_wrist['x'] += 1
        self.torso['x'] += 1
        self.update_circles()
        self.set_button_text()

    def print_pos(self, event):  # Print mouse position on image to the console when mouse is clicked
        x = int(event.x / (1000 / 224))  # normalize the coordinates between 0 and 224
        y = int(event.y / (1000 / 224))
        if self.selected_joint == 0:
            self.head['x'] = x
            self.head['y'] = y
            print(f'Head x: {self.head["x"]} y: {self.head["y"]}')
            self.head_button.config(text=f'Head x: {self.head["x"]} y: {self.head["y"]}')

            self.canvas.coords(self.head_circle, self.head['x'] * 1000 / 224, self.head['y'] * 1000 / 224,
                               self.head['x'] * 1000 / 224 + 10, self.head['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 1:
            self.left_ankle['x'] = x
            self.left_ankle['y'] = y
            print(f'Left ankle x: {self.left_ankle["x"]} y: {self.left_ankle["y"]}')
            self.left_ankle_button.config(text=f'Left ankle x: {self.left_ankle["x"]} y: {self.left_ankle["y"]}')

            self.canvas.coords(self.left_ankle_circle, self.left_ankle['x'] * 1000 / 224, self.left_ankle['y'] * 1000 / 224,
                               self.left_ankle['x'] * 1000 / 224 + 10, self.left_ankle['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 2:
            self.left_elbow['x'] = x
            self.left_elbow['y'] = y
            print(f'Left elbow x: {self.left_elbow["x"]} y: {self.left_elbow["y"]}')
            self.left_elbow_button.config(text=f'Left elbow x: {self.left_elbow["x"]} y: {self.left_elbow["y"]}')

            self.canvas.coords(self.left_elbow_circle, self.left_elbow['x'] * 1000 / 224, self.left_elbow['y'] * 1000 / 224,
                               self.left_elbow['x'] * 1000 / 224 + 10, self.left_elbow['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 3:
            self.left_hip['x'] = x
            self.left_hip['y'] = y
            print(f'Left hip x: {self.left_hip["x"]} y: {self.left_hip["y"]}')
            self.left_hip_button.config(text=f'Left hip x: {self.left_hip["x"]} y: {self.left_hip["y"]}')

            self.canvas.coords(self.left_hip_circle, self.left_hip['x'] * 1000 / 224, self.left_hip['y'] * 1000 / 224,
                               self.left_hip['x'] * 1000 / 224 + 10, self.left_hip['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 4:
            self.left_knee['x'] = x
            self.left_knee['y'] = y
            print(f'Left knee x: {self.left_knee["x"]} y: {self.left_knee["y"]}')
            self.left_knee_button.config(text=f'Left knee x: {self.left_knee["x"]} y: {self.left_knee["y"]}')

            self.canvas.coords(self.left_knee_circle, self.left_knee['x'] * 1000 / 224, self.left_knee['y'] * 1000 / 224,
                               self.left_knee['x'] * 1000 / 224 + 10, self.left_knee['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 5:
            self.left_shoulder['x'] = x
            self.left_shoulder['y'] = y
            print(f'Left shoulder x: {self.left_shoulder["x"]} y: {self.left_shoulder["y"]}')
            self.left_shoulder_button.config(text=f'Left shoulder x: {self.left_shoulder["x"]} y: {self.left_shoulder["y"]}')

            self.canvas.coords(self.left_shoulder_circle, self.left_shoulder['x'] * 1000 / 224, self.left_shoulder['y'] * 1000 / 224,
                               self.left_shoulder['x'] * 1000 / 224 + 10, self.left_shoulder['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 6:
            self.left_wrist['x'] = x
            self.left_wrist['y'] = y
            print(f'Left wrist x: {self.left_wrist["x"]} y: {self.left_wrist["y"]}')
            self.left_writs_button.config(text=f'Left wrist x: {self.left_wrist["x"]} y: {self.left_wrist["y"]}')

            self.canvas.coords(self.left_wrist_circle, self.left_wrist['x'] * 1000 / 224, self.left_wrist['y'] * 1000 / 224,
                               self.left_wrist['x'] * 1000 / 224 + 10, self.left_wrist['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 7:
            self.neck['x'] = x
            self.neck['y'] = y
            print(f'Neck x: {self.neck["x"]} y: {self.neck["y"]}')
            self.neck_button.config(text=f'Neck x: {self.neck["x"]} y: {self.neck["y"]}')

            self.canvas.coords(self.neck_circle, self.neck['x'] * 1000 / 224, self.neck['y'] * 1000 / 224,
                               self.neck['x'] * 1000 / 224 + 10, self.neck['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 8:
            self.right_ankle['x'] = x
            self.right_ankle['y'] = y
            print(f'Right ankle x: {self.right_ankle["x"]} y: {self.right_ankle["y"]}')
            self.right_ankle_button.config(text=f'Right ankle x: {self.right_ankle["x"]} y: {self.right_ankle["y"]}')

            self.canvas.coords(self.right_ankle_circle, self.right_ankle['x'] * 1000 / 224, self.right_ankle['y'] * 1000 / 224,
                               self.right_ankle['x'] * 1000 / 224 + 10, self.right_ankle['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 9:
            self.right_elbow['x'] = x
            self.right_elbow['y'] = y
            print(f'Right elbow x: {self.right_elbow["x"]} y: {self.right_elbow["y"]}')
            self.right_elbow_button.config(text=f'Right elbow x: {self.right_elbow["x"]} y: {self.right_elbow["y"]}')

            self.canvas.coords(self.right_elbow_circle, self.right_elbow['x'] * 1000 / 224, self.right_elbow['y'] * 1000 / 224,
                               self.right_elbow['x'] * 1000 / 224 + 10, self.right_elbow['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 10:
            self.right_hip['x'] = x
            self.right_hip['y'] = y
            print(f'Right hip x: {self.right_hip["x"]} y: {self.right_hip["y"]}')
            self.right_hip_button.config(text=f'Right hip x: {self.right_hip["x"]} y: {self.right_hip["y"]}')

            self.canvas.coords(self.right_hip_circle, self.right_hip['x'] * 1000 / 224, self.right_hip['y'] * 1000 / 224,
                               self.right_hip['x'] * 1000 / 224 + 10, self.right_hip['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 11:
            self.right_knee['x'] = x
            self.right_knee['y'] = y
            print(f'Right knee x: {self.right_knee["x"]} y: {self.right_knee["y"]}')
            self.right_knee_button.config(text=f'Right knee x: {self.right_knee["x"]} y: {self.right_knee["y"]}')

            self.canvas.coords(self.right_knee_circle, self.right_knee['x'] * 1000 / 224, self.right_knee['y'] * 1000 / 224,
                               self.right_knee['x'] * 1000 / 224 + 10, self.right_knee['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 12:
            self.right_shoulder['x'] = x
            self.right_shoulder['y'] = y
            print(f'Right shoulder x: {self.right_shoulder["x"]} y: {self.right_shoulder["y"]}')
            self.right_shoulder_button.config(text=f'Right shoulder x: {self.right_shoulder["x"]} y: {self.right_shoulder["y"]}')

            self.canvas.coords(self.right_shoulder_circle, self.right_shoulder['x'] * 1000 / 224, self.right_shoulder['y'] * 1000 / 224,
                               self.right_shoulder['x'] * 1000 / 224 + 10, self.right_shoulder['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 13:
            self.right_wrist['x'] = x
            self.right_wrist['y'] = y
            print(f'Right wrist x: {self.right_wrist["x"]} y: {self.right_wrist["y"]}')
            self.right_writs_button.config(text=f'Right wrist x: {self.right_wrist["x"]} y: {self.right_wrist["y"]}')

            self.canvas.coords(self.right_wrist_circle, self.right_wrist['x'] * 1000 / 224, self.right_wrist['y'] * 1000 / 224,
                               self.right_wrist['x'] * 1000 / 224 + 10, self.right_wrist['y'] * 1000 / 224 + 10)
        elif self.selected_joint == 14:
            self.torso['x'] = x
            self.torso['y'] = y
            print(f'Torso x: {self.torso["x"]} y: {self.torso["y"]}')
            self.torso_button.config(text=f'Torso x: {self.torso["x"]} y: {self.torso["y"]}')

            self.canvas.coords(self.torso_circle, self.torso['x'] * 1000 / 224, self.torso['y'] * 1000 / 224,
                               self.torso['x'] * 1000 / 224 + 10, self.torso['y'] * 1000 / 224 + 10)

        print("Mouse clicked at: ", x, y)

    def get_json(self):
        """Open json file and read the data into self.json_dict"""
        with open(self.json_dir, 'r') as json_file:
            self.json_dict = json.load(json_file)
        # print(f'Json file loaded, {self.json_dict}')

    def save_pose(self):
        """Saves the pose in the json file"""
        pose = {'head': self.head, 'image': f'{self.image}', 'left_ankle': self.left_ankle,
                'left_elbow': self.left_elbow, 'left_hip': self.left_hip,
                'left_knee': self.left_knee, 'left_shoulder': self.left_shoulder, 'left_wrist': self.left_wrist,
                'neck': self.neck, 'right_ankle': self.right_ankle, 'right_elbow': self.right_elbow, 'right_hip': self.right_hip,
                'right_knee': self.right_knee, 'right_shoulder': self.right_shoulder, 'right_writs': self.right_wrist,
                'torso': self.torso}
        print(pose)
        # write pose to json file
        self.json_pose[f'image{self.index}'] = pose
        """add pose to json_dict"""
        self.json_dict[f'image{self.index}'] = pose
        with open(self.json_dir, 'w') as json_file:
            json.dump(self.json_dict, json_file, indent=3)

        print("Save data selected")

    def key_pressed(self, event):
        print(f"Key pressed: {event.char}")
        if event.char == 'r' or event.char == ',':
            self.save_pose()
        elif event.char == 'e' or event.char == 'o':
            self.next_data()
        elif event.char == 'q' or event.char == 'u':
            self.prev_data()
        elif event.char == 'j':
            if self.selected_joint == 0:
                self.selected_joint = 14
                self.update_joint_text()
            else:
                self.selected_joint = self.selected_joint - 1
                self.update_joint_text()
        elif event.char == 'l':
            if self.selected_joint == 14:
                self.selected_joint = 0
                self.update_joint_text()
            else:
                self.selected_joint = self.selected_joint + 1
                self.update_joint_text()
        elif event.char == 'g' or event.char == 'p':
            self.get_previous_pose()
        elif event.char == '1':
            self.move_pose_left()
        elif event.char == '4':
            self.move_pose_right()
        elif event.char == '2':
            self.move_pose_up()
        elif event.char == '3':
            self.move_pose_down()
        elif event.char == 'f':
            self.set_predicted_pose()
        elif event.char == 'z':
            self.zero_current()
        elif event.char == 's':
            self.move_current_down()
        elif event.char == 'w':
            self.move_current_up()
        elif event.char == 'a':
            self.move_current_left()
        elif event.char == 'd':
            self.move_current_right()
        elif event.char == 'v':
            self.switch_sides()
        elif event.char == 't':
            self.get_next_pose()
        elif event.char == '0':
            self.skip_hundred()

    def switch_sides(self):
        """swap left and right side coordinates"""
        self.left_shoulder, self.right_shoulder = self.right_shoulder, self.left_shoulder
        self.left_elbow, self.right_elbow = self.right_elbow, self.left_elbow
        self.left_wrist, self.right_wrist = self.right_wrist, self.left_wrist
        self.left_hip, self.right_hip = self.right_hip, self.left_hip
        self.left_knee, self.right_knee = self.right_knee, self.left_knee
        self.left_ankle, self.right_ankle = self.right_ankle, self.left_ankle


        self.set_button_text()
        self.update_circles()

    def set_predicted_pose(self):
        """"nose, left eye, right eye, left ear, right ear, left shoulder, right shoulder, left elbow, right elbow,
        left wrist, right wrist, left hip, right hip, left knee, right knee, left ankle, right ankle"""
        pose = predict_pose_movenet(f'{self.img_dir}{self.image}')
        """unpack pose"""
        print(pose)
        print(pose[0][0][0][0])
        print(pose[0][0][1][0])
        self.head['x'] = int(224 - (pose[0][0][0][0]*224))
        self.head['y'] = int(pose[0][0][0][1]*224)
        self.left_ankle['x'] = int(224 - (pose[0][0][15][0]*224))
        self.left_ankle['y'] = int(pose[0][0][15][1]*224)
        self.left_elbow['x'] = int(224 - (pose[0][0][7][0]*224))
        self.left_elbow['y'] = int(pose[0][0][7][1]*224)
        self.left_hip['x'] = int(224 - (pose[0][0][11][0]*224))
        self.left_hip['y'] = int(pose[0][0][11][1]*224)
        self.left_knee['x'] = int(224 - (pose[0][0][13][0]*224))
        self.left_knee['y'] = int(pose[0][0][13][1]*224)
        self.left_shoulder['x'] = int(224 - (pose[0][0][5][0]*224))
        self.left_shoulder['y'] = int(pose[0][0][5][1]*224)
        self.left_wrist['x'] = int(224 - (pose[0][0][9][0]*224))
        self.left_wrist['y'] = int(pose[0][0][9][1]*224)
        # self.neck['x'] = int(pose[0][7][0])
        # self.neck['y'] = int(pose[0][7][1])
        self.right_ankle['x'] = int(224 - (pose[0][0][16][0]*224))
        self.right_ankle['y'] = int(pose[0][0][16][1]*224)
        self.right_elbow['x'] = int(224 - (pose[0][0][8][0]*224))
        self.right_elbow['y'] = int(pose[0][0][8][1]*224)
        self.right_hip['x'] = int(224 - (pose[0][0][12][0]*224))
        self.right_hip['y'] = int(pose[0][0][12][1]*224)
        self.right_knee['x'] = int(224 - (pose[0][0][14][0]*224))
        self.right_knee['y'] = int(pose[0][0][14][1]*224)
        self.right_shoulder['x'] = int(224 - (pose[0][0][6][0]*224))
        self.right_shoulder['y'] = int(pose[0][0][6][1]*224)
        self.right_wrist['x'] = int(224 - (pose[0][0][10][0]*224))
        self.right_wrist['y'] = int(pose[0][0][10][1]*224)
        """flip all coordinates"""

        # self.head['y'] = 224 - self.head['y']
        # self.torso['x'] = int(pose[0][14][0])
        # self.torso['y'] = int(pose[0][14][1])
        self.set_button_text()
        self.update_circles()
        # print(pose)
        # print(self.head)

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

    def update_circles(self):
        self.canvas.coords(self.head_circle, self.head['x'] * 1000 / 224, self.head['y'] * 1000 / 224,
                           self.head['x'] * 1000 / 224 + 10, self.head['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.left_ankle_circle, self.left_ankle['x'] * 1000 / 224, self.left_ankle['y'] * 1000 / 224,
                           self.left_ankle['x'] * 1000 / 224 + 10, self.left_ankle['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.left_elbow_circle, self.left_elbow['x'] * 1000 / 224, self.left_elbow['y'] * 1000 / 224,
                           self.left_elbow['x'] * 1000 / 224 + 10, self.left_elbow['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.left_hip_circle, self.left_hip['x'] * 1000 / 224, self.left_hip['y'] * 1000 / 224,
                           self.left_hip['x'] * 1000 / 224 + 10, self.left_hip['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.left_knee_circle, self.left_knee['x'] * 1000 / 224, self.left_knee['y'] * 1000 / 224,
                           self.left_knee['x'] * 1000 / 224 + 10, self.left_knee['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.left_shoulder_circle, self.left_shoulder['x'] * 1000 / 224,
                           self.left_shoulder['y'] * 1000 / 224,
                           self.left_shoulder['x'] * 1000 / 224 + 10, self.left_shoulder['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.left_wrist_circle, self.left_wrist['x'] * 1000 / 224, self.left_wrist['y'] * 1000 / 224,
                           self.left_wrist['x'] * 1000 / 224 + 10, self.left_wrist['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.neck_circle, self.neck['x'] * 1000 / 224, self.neck['y'] * 1000 / 224,
                           self.neck['x'] * 1000 / 224 + 10, self.neck['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.right_ankle_circle, self.right_ankle['x'] * 1000 / 224,
                           self.right_ankle['y'] * 1000 / 224,
                           self.right_ankle['x'] * 1000 / 224 + 10, self.right_ankle['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.right_elbow_circle, self.right_elbow['x'] * 1000 / 224,
                           self.right_elbow['y'] * 1000 / 224,
                           self.right_elbow['x'] * 1000 / 224 + 10, self.right_elbow['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.right_hip_circle, self.right_hip['x'] * 1000 / 224, self.right_hip['y'] * 1000 / 224,
                           self.right_hip['x'] * 1000 / 224 + 10, self.right_hip['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.right_knee_circle, self.right_knee['x'] * 1000 / 224, self.right_knee['y'] * 1000 / 224,
                           self.right_knee['x'] * 1000 / 224 + 10, self.right_knee['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.right_shoulder_circle, self.right_shoulder['x'] * 1000 / 224,
                           self.right_shoulder['y'] * 1000 / 224,
                           self.right_shoulder['x'] * 1000 / 224 + 10, self.right_shoulder['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.right_wrist_circle, self.right_wrist['x'] * 1000 / 224,
                           self.right_wrist['y'] * 1000 / 224,
                           self.right_wrist['x'] * 1000 / 224 + 10, self.right_wrist['y'] * 1000 / 224 + 10)
        self.canvas.coords(self.torso_circle, self.torso['x'] * 1000 / 224, self.torso['y'] * 1000 / 224,
                           self.torso['x'] * 1000 / 224 + 10, self.torso['y'] * 1000 / 224 + 10)