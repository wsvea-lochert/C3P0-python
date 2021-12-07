import tensorflow as tf
import cv2
import numpy as np

model = tf.keras.models.load_model('models/CNN_MODEL_ARCH')  # loading our model.


def predict_pose(image):
    """
    Predict the pose of the image.
    """
    return model.predict(load_image(image)).reshape(1, 15, 2) * 224


def load_image(image_path):
    image = cv2.imread(image_path)
    image_color = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resize = cv2.resize(image_color, (224, 224))
    img = np.array(image_resize).reshape(-1, 224, 224, 3)
    return img

