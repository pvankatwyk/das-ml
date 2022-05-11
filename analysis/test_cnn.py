import tensorflow as tf
import cv2
import re
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
import os

color_mode = 'rgb'
model_path = "event_model_2.h5"
model = tf.keras.models.load_model(model_path)

dir = 'F:/Research/DAS/event_detection_dataset/eq_vs_none_augmented/train/EQ/'
# dir = r"F:\Research\DAS\event_detection_augmented\eq_vs_none\train/EQ/"
def make_prediction(image_fp):
    # im = cv2.imread(image_fp)  # load image
    # plt.imshow(im)
    # plt.show()
    img = image.load_img(image_fp, target_size=(256, 256), color_mode=color_mode)
    img = image.img_to_array(img)

    image_array = img / 255.  # scale the image
    img_batch = np.expand_dims(image_array, axis=0)

    class_ = ['EQ', 'None']  # possible output values
    predicted_value = class_[model.predict(img_batch).argmax()]
    true_value = re.search(r'(EQ)|(None)', image_fp)[0]

    out = f"""Predicted: {predicted_value}
    True: {true_value}
    Correct?: {predicted_value == true_value}"""

    return out, true_value, predicted_value


total_count = 0
correct_count = 0
for element in os.listdir(dir):
    out, true_value, predicted_value = make_prediction(dir + element)
    print(element, out)
    if true_value == predicted_value:
        correct_count += 1
    else:
        stop = ''
    total_count += 1

print(correct_count / total_count)