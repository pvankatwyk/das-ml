# Script for taking DAS photos and cataloged event times and cropping the photo to the event

import os
import pandas as pd
import time
import tensorflow as tf


def identify_cataloged_events():
    photo_dir = r"F:/Research/DAS/photos/"
    photos = os.listdir(photo_dir)
    catalog = pd.read_csv(r'../src/DAS_Catalog.csv')
    catalog['photo'] = catalog['Filename'].apply(lambda x: x[-19:-4] + ".png")
    catalog['time (s)'] = catalog['Sample in file (P-arrival)'] / 2000  # Hz

    start = time.time()
    count = 0
    for photo in photos:
        print(
            f"Cropping: {photo}, Count: {count}/180, Elapsed Time: {round((time.time() - start) / 60.0, 4)} minutes.")

        # Load image
        image_fp = photo_dir + photo
        img = tf.keras.utils.load_img(image_fp)

        # Find the pixel in the photo where the event occurs (seconds to pixels)
        pixels_per_second = img.size[0] / 15.0  # seconds
        event_seconds = catalog['time (s)'][catalog['photo'] == photo].values[0]
        event_pixel = event_seconds * pixels_per_second

        # Create a cushion of 1 second on either side
        time_cushion = 2  # second
        event_right = max([event_pixel + (time_cushion * pixels_per_second), 0])
        event_left = max([event_pixel - (time_cushion * pixels_per_second), 0])

        # Subset photo based on above cushion
        try:
            bbox = (event_left, 0, event_right, img.size[1])  # (x1, y1, x2, y2)
            im = img.crop(bbox)
            im.save(f"../src/photos/{photo}")
        except SystemError:
            pass
        count += 1


if __name__ == "__main__":
    identify_cataloged_events()
