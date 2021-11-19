import os
# from PIL import Image


# Open a folder and read all the files in it
def read_folder(folder):
    images = []
    for image in os.listdir(folder):
        if image.endswith(".png"):
            images.append(image)
    return images


"""Open an image using Pillow"""
# def open_image(image_path):
#     return Image.open(image_path)


"""Print mouse position on image to the console when mouse is clicked"""
def print_pos(event):
    print("Mouse clicked at: ", event.x, event.y)
