import streamlit as st
from PIL import Image
import pytesseract
import re
import requests
import math

# ========== CONFIG ==========
API_KEY = "c9f17577ae7638ef95d7eed260575c2a"  # replace with your key
DEFAULT_CITY = "Dhaka"

st.set_page_config(page_title="OCR Weather Compare", page_icon="🌡️")

st.title("🌡️ OCR Temperature vs Live Weather")
st.write("Upload or capture an image showing temperature, and compare it with live weather data.")

# ========== UPLOAD / CAMERA ==========
uploaded_file = st.file_uploader("📂 Upload an image", type=["jpg", "jpeg", "png"])
camera_file = st.camera_input("📸 Take a photo")

# Choose file (camera has priority if both provided)
img_file = camera_file or uploaded_file

if img_file is not None:
    # Load image
    image = Image.open(img_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR
    text = pytesseract.image_to_string(image)
    st.write("📝 Extracted Text:", text)

    # Regex temperature detection
    pattern = re.search(
        r'(\d+(?:\.\d+)?)\s*(?:°\s*[Cc]|degrees?\s*C(?:elsius)?|deg\s*C|C\b)',
        text,
        re.IGNORECASE,
    )

    if pattern:
        detected_temp_raw = float(pattern.group(1))

        # custom rounding (below .5 → floor, .5+ → ceil)
        if detected_temp_raw % 1 < 0.5:
            detected_temp = math.floor(detected_temp_raw)
        else:
            detected_temp = math.ceil(detected_temp_raw)

        st.success(f"📸 OCR Detected Temp: {detected_temp_raw} → {detected_temp} °C")

        # Weather API
        city = st.text_input("🌍 Enter city", DEFAULT_CITY)
        if st.button("Compare with Live Weather"):
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url).json()

            if "main" in response:
                current_temp = round(response["main"]["temp"])
                st.info(f"🌍 Current Temp in {city}: {current_temp} °C")

                # Compare
                if detected_temp == current_temp:
                    st.success("✅ Match: Image temperature equals current temperature")
                else:
                    diff = abs(detected_temp - current_temp)
                    st.error(f"❌ Mismatch: OCR={detected_temp} °C vs API={current_temp} °C (Diff={diff}°)")
            else:
                st.error(f"⚠️ Weather API Error: {response.get('message', 'Unknown error')}")

    else:
        st.error("❌ No temperature detected in image.")
