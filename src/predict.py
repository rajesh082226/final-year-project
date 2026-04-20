from location_generator import generate_random_location
from arcgis_map import open_arcgis_map

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

import serial
import time
import os

# -------------------------------------------------
# SERIAL CONNECTION (Arduino)
# -------------------------------------------------
ser = serial.Serial('COM3', 9600)   # change COM port if needed
time.sleep(2)

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

MODEL_PATH = os.path.join(PROJECT_DIR, "models", "fire_campfire_model.h5")

print("Loading model from:", MODEL_PATH)

model = tf.keras.models.load_model(MODEL_PATH)

classes = ["fire", "no_fire"]

# -------------------------------------------------
# SENSOR FUNCTION
# -------------------------------------------------
def read_flame_sensor():

    data = ser.readline().decode('utf-8').strip()

    print("Sensor Data:", data)

    if data == "FLAME_DETECTED":
        return True
    else:
        return False


# -------------------------------------------------
# IMAGE PREDICTION FUNCTION
# -------------------------------------------------
def predict_image(img_path):

    img = image.load_img(img_path, target_size=(224,224))
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img, verbose=0)

    label = classes[np.argmax(pred)]
    confidence = np.max(pred)

    return label, confidence


# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------
if __name__ == "__main__":

    sample_image = os.path.join(PROJECT_DIR, "sample.jpg")

    label, confidence = predict_image(sample_image)

    print("Model Prediction:", label)
    print("Confidence:", confidence)

    flame_detected = read_flame_sensor()

    # -------------------------------------------------
    # FINAL DECISION
    # -------------------------------------------------
    if label == "fire" and flame_detected:

        print("\n🔥 FIRE CONFIRMED (MODEL + SENSOR)")

        lat, lon = generate_random_location()

        print("Latitude:", lat)
        print("Longitude:", lon)

        open_arcgis_map(lat, lon)

    else:

        print("\n✅ No Fire Detected")