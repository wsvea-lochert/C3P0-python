from tkinter import Button


def make_buttons(root, btns, h, w, canvas):
    right_writs_button = Button(root, text="Right Writs", command=btns.right_wrist, height=2, width=20, bg="#C7463D", fg='white')
    right_writs_button.place(x=w/1.4, y=h/3)

    right_elbow_button = Button(root, text="Right Elbow", command=btns.right_elbow, height=2, width=20, bg="#C7463D", fg='white')
    right_elbow_button.place(x=w/1.4, y=h/3.5)

    right_shoulder_button = Button(root, text="Right Shoulder", command=btns.right_shoulder, height=2, width=20, bg="#C7463D", fg='white')
    right_shoulder_button.place(x=w/1.4, y=h/5)

    right_hip_button = Button(root, text="Right Hip", command=btns.right_hip, height=2, width=20, bg="#C7463D", fg='white')
    right_hip_button.place(x=w/1.4, y=h/2.5)

    right_knee_button = Button(root, text="Right Knee", command=btns.right_knee, height=2, width=20, bg="#C7463D", fg='white')
    right_knee_button.place(x=w/1.4, y=h/2)

    right_ankle_button = Button(root, text="Right Ankle", command=btns.right_ankle, height=2, width=20, bg="#C7463D", fg='white')
    right_ankle_button.place(x=w/1.4, y=h/1.7)

    left_writs_button = Button(root, text="Left Writs", command=btns.left_wrist, height=2, width=20, bg='#3D84C7', fg='white')
    left_writs_button.place(x=w/5.4, y=h/3)

    left_elbow_button = Button(root, text="Left Elbow", command=btns.left_elbow, height=2, width=20, bg='#3D84C7', fg='white')
    left_elbow_button.place(x=w/5.4, y=h/3.5)

    left_shoulder_button = Button(root, text="Left Shoulder", command=btns.left_shoulder, height=2, width=20, bg='#3D84C7', fg='white')
    left_shoulder_button.place(x=w/5.4, y=h/5)

    left_hip_button = Button(root, text="Left Hip", command=btns.left_hip, height=2, width=20, bg='#3D84C7', fg='white')
    left_hip_button.place(x=w/5.4, y=h/2.5)

    left_knee_button = Button(root, text="Left Knee", command=btns.left_knee, height=2, width=20, bg='#3D84C7', fg='white')
    left_knee_button.place(x=w/5.4, y=h/2)

    left_ankle_button = Button(root, text="Left Ankle", command=btns.left_ankle, height=2, width=20, bg='#3D84C7', fg='white')
    left_ankle_button.place(x=w/5.4, y=h/1.7)

    torso_button = Button(root, text="Torso", command=btns.torso, height=2, width=20, bg='#B63DC7', fg='white')
    torso_button.place(x=w/2.2, y=h/1.2)

    head_button = Button(root, text="Head", command=btns.head, height=2, width=20, bg='#B63DC7', fg='white')
    head_button.place(x=w/2.5, y=h/13)

    neck_button = Button(root, text="Neck", command=btns.neck, height=2, width=20, bg='#B63DC7', fg='white')
    neck_button.place(x=w/2, y=h/13)

    save_button = Button(root, text="Save", command=btns.save_data, height=3, width=20, bg="green", fg="white")
    save_button.place(x=w/1.4, y=h/1.3)

    # Buttons for handling moving through the data
    next_button = Button(root, text="Next", command=lambda: btns.next_data(canvas), height=3, width=20, bg="#11EA9B", fg="black")
    next_button.place(x=w/2, y=h/50)

    prev_button = Button(root, text="Prev", command=lambda: btns.prev_data(canvas), height=3, width=20, bg="#EAC611", fg="black")
    prev_button.place(x=w/2.5, y=h/50)


