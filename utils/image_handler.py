import os
# from PIL import Image


# Open a folder and read all the files in it
def read_folder(folder):
    images = []
    for image in os.listdir(folder):
        images.append(image)
    return images


def print_pos(event):                # Print mouse position on image to the console when mouse is clicked
    x = int(event.x / (1000/224))    # normalize the coordinates between 0 and 224
    y = int(event.y / (1000/224))
    print("Mouse clicked at: ", x, y)
