# 🌡️ OCR Weather Compare App

A Streamlit web app that:
- 📸 Captures or uploads an image (camera/gallery)
- 🔍 Extracts temperature from the image using **Tesseract OCR**
- 🌍 Fetches live weather temperature from **OpenWeather API**
- ✅ Compares both values and shows the result

---

---

## ⚙️ Features
- Upload an image **or** capture directly with device camera
- OCR detects temperatures in formats like:
  - `23°C`
  - `23 °C`
  - `23 degree Celsius`
  - `38.5°C`
- Rounds decimals (38.3 → 38, 38.5 → 39)
- Fetches real-time weather data from [OpenWeather](https://openweathermap.org/)
- Compares OCR-detected temperature with live temperature

---

## 🛠 Installation (Local)

### 1. Clone the repo
```bash
git clone https://github.com/Prinom2000/ocr-weather-app.git
cd ocr-weather-app
