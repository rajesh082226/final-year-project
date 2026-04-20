import tensorflow as tf
import numpy as np
import serial
import time
import os
from tensorflow.keras.preprocessing import image
from twilio.rest import Client
from gps_location import get_location_from_image
from arcgis_map import open_arcgis_map

# -------------------------------------------------
# PATH SETUP
# -------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

MODEL_PATH = os.path.join(PROJECT_DIR, "models", "fire_campfire_model.h5")
FIRE_IMAGE = os.path.join(PROJECT_DIR, "sample.jpg")   # for AI prediction
GPS_IMAGE  = os.path.join(PROJECT_DIR, "gps_photo.jpeg") # for GPS location

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
print("Loading model from:", MODEL_PATH)
model = tf.keras.models.load_model(MODEL_PATH)
classes = ["fire", "no_fire"]

# -------------------------------------------------
# TWILIO CONFIG
# -------------------------------------------------
ACCOUNT_SID   = "REMOVED_SECRET"
AUTH_TOKEN    = "REMOVED_SECRET"
TWILIO_NUMBER = "+19854127043"
TO_NUMBER     = "+916303246692"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# -------------------------------------------------
# SERIAL SETUP
# -------------------------------------------------
try:
    print("Connecting to Arduino on COM12...")
    arduino = serial.Serial("COM12", 9600, timeout=1)
    time.sleep(5)
    arduino.reset_input_buffer()
    print("Arduino connected and ready\n")
except Exception as e:
    print("Error connecting:", e)
    exit()

# -------------------------------------------------
# IMAGE PREDICTION FUNCTION
# -------------------------------------------------
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img, verbose=0)
    label = classes[np.argmax(pred)]
    confidence = np.max(pred)
    return label, confidence

# -------------------------------------------------
# SENSOR MONITORING FUNCTION
# -------------------------------------------------
def read_flame_sensor(timeout=30):
    print("Monitoring sensor...\n")
    start = time.time()
    flame_detected = False

    while time.time() - start < timeout:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode(errors='ignore').strip()
            if line:
                print("Sensor:", line)
            if line == "FLAME_DETECTED":
                flame_detected = True
        time.sleep(0.1)

    return flame_detected

# -------------------------------------------------
# SMS ALERT FUNCTION
# -------------------------------------------------
def send_alert(lat, lon):
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    print("\nSending SMS alert...")
    client.messages.create(
        body=f"🚨 ALERT: Forest Fire Detected!\nLocation: {maps_link}",
        from_=TWILIO_NUMBER,
        to=TO_NUMBER
    )
    print("SMS sent successfully")

# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------
if __name__ == "__main__":

    # Step 1 - Get GPS location from phone image
    lat, lon = get_location_from_image(GPS_IMAGE)

    # Step 2 - AI prediction on fire image
    label, confidence = predict_image(FIRE_IMAGE)

    # Step 3 - Sensor monitoring
    flame_detected = read_flame_sensor(timeout=30)

    print("\n==============================")
    print("AI Prediction :", label)
    print("Confidence    :", f"{confidence*100:.2f}%")
    print("Sensor Status :", "FLAME_DETECTED" if flame_detected else "NO_FLAME")
    print("Location      :", lat, lon)
    print("==============================")

    # Final Decision
    if label == "fire" and flame_detected:
        print("\n🔥 FIRE CONFIRMED (AI + SENSOR)")

        # Send SMS with location
        send_alert(lat, lon)

        print("Latitude :", lat)
        print("Longitude:", lon)

        # Open ArcGIS map
        open_arcgis_map(lat, lon)

        # Send alert to Arduino
        arduino.write(b'ALERT\n')

    else:
        print("\n✅ No Fire Confirmed")
        arduino.write(b'NO_ALERT\n')

    # Cleanup
    arduino.close()
    print("\nSystem Stopped")