# 🔥 Forest Fire Detection & Alert System

A real-time forest fire detection system that combines **AI image classification**, **IoT flame sensors (Arduino)**, and **GPS-based SMS alerts** to detect and report forest fires automatically.

---

## 🧠 How It Works

The system uses a **dual-confirmation approach** — a fire is only confirmed when **both** the AI model **and** the hardware sensor agree:

```
📷 Camera Image  →  MobileNetV2 CNN  →  AI Prediction (Fire / No Fire)
🔥 Flame Sensor  →  Arduino (COM12)  →  Hardware Detection
📍 GPS Photo     →  EXIF Metadata    →  Location Coordinates
         ↓
  Both Confirm Fire?
         ↓
📲 Twilio SMS Alert with Google Maps Link
🗺️  ArcGIS Map Opens Automatically
🔔 Arduino Buzzer + LED Activated
```

---

## ✨ Features

- **AI Fire Classification** — MobileNetV2 CNN trained to classify `fire`, `campfire`, and `no_fire` from images
- **IoT Flame Sensor** — Arduino reads a hardware flame sensor and holds detection for 60 seconds
- **GPS Location Extraction** — Extracts coordinates from image EXIF metadata
- **SMS Alert** — Sends a Twilio SMS with a Google Maps link to the fire location
- **ArcGIS Map** — Automatically opens an ArcGIS map pinpointing the fire
- **Arduino Feedback** — Sends `ALERT` or `NO_ALERT` signal back to Arduino to trigger buzzer and LED

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| AI Model | TensorFlow / Keras — MobileNetV2 |
| Hardware | Arduino (flame sensor, buzzer, LED) |
| Serial Communication | PySerial |
| SMS Alerts | Twilio API |
| GPS Extraction | EXIF metadata from image |
| Mapping | ArcGIS + Google Maps |
| Language | Python 3.x + Arduino C++ |

---

## 📁 Project Structure

```
forest-fire-project/
├── models/
│   └── fire_campfire_model.h5      # Trained MobileNetV2 model
├── src/
│   ├── fire_prediction.py          # Main program
│   ├── model_builder.py            # MobileNetV2 model architecture
│   ├── gps_location.py             # GPS extraction from image EXIF
│   └── arcgis_map.py               # ArcGIS map integration
├── arduino/
│   └── flame_sensor.ino            # Arduino sketch
├── sample.jpg                      # Test image for AI prediction
├── gps_photo.jpeg                  # Image with GPS EXIF for location
├── .env                            # API credentials (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.8+
- Arduino IDE
- Twilio account — [sign up here](https://www.twilio.com)
- Arduino board with flame sensor, buzzer, and LED connected

### Hardware Setup

Connect to Arduino as follows:

| Component | Arduino Pin |
|---|---|
| Flame Sensor | Pin 7 |
| Buzzer | Pin 8 |
| LED | Pin 9 |

Upload `arduino/flame_sensor.ino` using the Arduino IDE. Connect Arduino via USB (default port: `COM12`).

### Python Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rajesh082226/final-year-project.git
   cd final-year-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_NUMBER=your_twilio_number
   TO_NUMBER=your_phone_number
   ```

4. **Add your trained model**

   Place `fire_campfire_model.h5` inside the `models/` folder.

5. **Run the system**
   ```bash
   python src/fire_prediction.py
   ```

---

## 🤖 AI Model

The model is built on **MobileNetV2** (pretrained on ImageNet) with custom classification layers:

- Input size: `224 x 224 x 3`
- Base: MobileNetV2 (frozen layers)
- Custom head: GlobalAveragePooling → Dense(128, ReLU) → Dense(3, Softmax)
- Classes: `fire`, `campfire`, `no_fire`
- Optimizer: Adam | Loss: Categorical Crossentropy

---

## 📲 Alert Example

When fire is confirmed by both AI and sensor, an SMS is sent:

```
🚨 ALERT: Forest Fire Detected!
Location: https://www.google.com/maps?q=17.3850,78.4867
```

---

## 🔐 Security

All sensitive credentials (Twilio SID, Auth Token, phone numbers) are stored in a `.env` file and excluded from version control via `.gitignore`.

> ⚠️ Never hardcode API keys directly in source files.

---

## 📜 License

This project was developed as a Final Year Project for academic purposes.

---

## 👤 Author

**Rajesh** — [GitHub](https://github.com/rajesh082226)
