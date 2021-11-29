import os
# from PIL import Image


# Open a folder and read all the files in it
def read_folder(folder):
    images = []
    for image in os.listdir(folder):
        images.append(image)
    return images



