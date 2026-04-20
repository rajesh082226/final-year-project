import pytesseract
from PIL import Image
import re

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_location_from_image(img_path):
    try:
        print("Reading GPS from image...")

        img = Image.open(img_path)

        # Crop bottom part where GPS text is shown
        width, height = img.size
        cropped = img.crop((0, int(height * 0.75), width, height))

        # Extract text
        text = pytesseract.image_to_string(cropped)

        print("Extracted text:", text)

        # Find Lat and Long values
        lat_match = re.search(r'Lat\s+([\d.]+)', text)
        lon_match = re.search(r'Long\s+([\d.]+)', text)

        if lat_match and lon_match:
            latitude  = float(lat_match.group(1))
            longitude = float(lon_match.group(1))

            print(f"Latitude  : {latitude}")
            print(f"Longitude : {longitude}")

            return latitude, longitude

        else:
            print("GPS text not found in image, using default")
            return 17.72999, 83.319003

    except Exception as e:
        print("Error reading image:", e)
        return 17.72999, 83.319003