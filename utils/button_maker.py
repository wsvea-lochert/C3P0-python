from tkinter import Button


def make_buttons(root, btns):
    right_writs_button = Button(root, text="Right Writs", command=btns.right_wrist)
    right_writs_button.pack()

    right_elbow_button = Button(root, text="Right Elbow", command=btns.right_elbow)
    right_elbow_button.pack()

    right_shoulder_button = Button(root, text="Right Shoulder", command=btns.right_shoulder)
    right_shoulder_button.pack()

    right_hip_button = Button(root, text="Right Hip", command=btns.right_hip)
    right_hip_button.pack()

    right_knee_button = Button(root, text="Right Knee", command=btns.right_knee)
    right_knee_button.pack()

    right_ankle_button = Button(root, text="Right Ankle", command=btns.right_ankle)
    right_ankle_button.pack()

    left_writs_button = Button(root, text="Left Writs", command=btns.left_wrist)
    left_writs_button.pack()

    left_elbow_button = Button(root, text="Left Elbow", command=btns.left_elbow)
    left_elbow_button.pack()

    left_shoulder_button = Button(root, text="Left Shoulder", command=btns.left_shoulder)
    left_shoulder_button.pack()

    left_hip_button = Button(root, text="Left Hip", command=btns.left_hip)
    left_hip_button.pack()

    left_knee_button = Button(root, text="Left Knee", command=btns.left_knee)
    left_knee_button.pack()

    left_ankle_button = Button(root, text="Left Ankle", command=btns.left_ankle)
    left_ankle_button.pack()

    torso_button = Button(root, text="Torso", command=btns.torso)
    torso_button.pack()

    head_button = Button(root, text="Head", command=btns.head)
    head_button.pack()

    neck_button = Button(root, text="Neck", command=btns.neck)
    neck_button.pack()

    save_button = Button(root, text="Save", command=btns.save_data)
    save_button.pack()