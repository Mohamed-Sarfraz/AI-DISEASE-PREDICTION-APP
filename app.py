
import streamlit as st
import serial
import time
import joblib
import numpy as np

# Load your AI Model
model = joblib.load('disease_predictor.pkl')

# Serial Setup
SERIAL_PORT = 'COM3'  # Change to your ESP32 COM port
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    st.success(f"Connected to {SERIAL_PORT} ✅")
except Exception as e:
    st.error(f"Failed to connect to serial port: {e}")

# Streamlit App Layout
st.title("🩺 AI-Based Disease Detection App")
st.subheader("Live Vitals Monitoring & Prediction")

placeholder = st.empty()

spo2_values = []
bpm_values = []
alerts = []

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line and "RED:" in line and "IR:" in line:
            parts = line.replace("RED:", "").replace("IR:", "").split("|")
            red = int(parts[0].strip())
            ir = int(parts[1].strip())

            # Simulate SpO₂ and BPM (simple method)
            spo2 = np.clip((red / ir) * 100, 85, 100)  # Simple SpO₂ estimation
            bpm = 75  # Simulated BPM (can be improved later)

            input_data = np.array([[spo2, bpm]])
            prediction = model.predict(input_data)[0]

            spo2_values.append(spo2)
            bpm_values.append(bpm)

            with placeholder.container():
                st.metric("SpO₂ (%)", round(spo2, 1))
                st.metric("BPM", bpm)

                if prediction == "Normal":
                    st.success("✅ Normal - No Disease Detected")
                else:
                    st.error(f"⚠️ Possible {prediction} Detected!")

            time.sleep(1)

    except Exception as e:
        st.error(f"Error reading from serial: {e}")
        break
