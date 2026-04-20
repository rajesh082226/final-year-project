import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Global constants
IMG_SIZE = (224, 224)
CLASS_NAMES = ["campfire", "forest_fire", "no_fire"]

# -------------------------------------------------
# Load trained model
# -------------------------------------------------
def load_trained_model(model_path="models/fire_campfire_model.h5"):
    """
    Loads and returns the trained CNN model
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError("❌ Model file not found")

    model = tf.keras.models.load_model(model_path)
    return model


# -------------------------------------------------
# Preprocess single image
# -------------------------------------------------
def preprocess_image(img_path):
    """
    Loads and preprocesses image for prediction
    """
    if not os.path.exists(img_path):
        raise FileNotFoundError("❌ Image file not found")

    img = image.load_img(img_path, target_size=IMG_SIZE)
    img = image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    return img


# -------------------------------------------------
# Predict class for single image
# -------------------------------------------------
def predict_fire_type(model, img_path):
    """
    Predicts No Fire / Campfire / Forest Fire
    """
    img = preprocess_image(img_path)
    prediction = model.predict(img)
    class_index = np.argmax(prediction)

    return CLASS_NAMES[class_index], prediction[0]


# -------------------------------------------------
# Get class labels from dataset folder
# -------------------------------------------------
def get_class_names_from_dir(train_dir="dataset/train"):
    """
    Reads class names from training directory
    """
    return sorted(os.listdir(train_dir))


# -------------------------------------------------
# Print prediction in readable format
# -------------------------------------------------
def pretty_print_prediction(class_name, confidence_array):
    """
    Prints prediction probabilities nicely
    """
    print("\n🔥 Prediction Result")
    print("----------------------")
    for i, prob in enumerate(confidence_array):
        print(f"{CLASS_NAMES[i]} : {prob*100:.2f}%")

    print(f"\n✅ Final Prediction: {class_name.upper()}")
