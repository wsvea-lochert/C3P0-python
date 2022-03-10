import tensorflow as tf
import cv2
import numpy as np
import tensorflow_hub as hub

# model = tf.keras.models.load_model('models/resnet_trainable_model')  # loading our model.
model = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
movenet = model.signatures['serving_default']




def predict_pose(image):
    """
    Predict the pose of the image.
    """
    return model.predict(load_image(image)).reshape(1, 15, 2) * 224


def predict_pose_movenet(path):
    print(f"Predicting pose using movenet... on image: {path}")
    # Load the input image.
    image_path = path
    image = tf.io.read_file(image_path)
    image = tf.compat.v1.image.decode_jpeg(image)
    image = tf.expand_dims(image, axis=0)
    # Resize and pad the image to keep the aspect ratio and fit the expected size.
    image = tf.cast(tf.image.resize_with_pad(image, 256, 256), dtype=tf.int32)
    # Run model inference.
    outputs = movenet(image)
    # Output is a [1, 1, 17, 3] tensor.
    keypoints = outputs['output_0']
    # print(keypoints)
    #return keypoints
    return keypoints.numpy()
    """
    nose, left eye, right eye, left ear, right ear, left shoulder, right shoulder, left elbow, 
    right elbow, left wrist, right wrist, left hip, right hip, left knee, right knee, left ankle, right ankle
    """





def load_image(image_path):
    image = cv2.imread(image_path)
    image_color = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resize = cv2.resize(image_color, (224, 224))
    img = np.array(image_resize).reshape(-1, 224, 224, 3)
    return img



