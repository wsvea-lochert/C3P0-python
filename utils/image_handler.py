import os


# Open a folder and read all the files in it
def read_folder(folder):
    images = []
    for image in os.listdir(folder):
        if image.endswith(".png"):
            images.append(image)
    return images