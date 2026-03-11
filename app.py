import streamlit as st
import joblib
import numpy as np
import requests

st.set_page_config(page_title="GreenAI AirSense", layout="centered")

st.title("🌍 GreenAI AirSense")
st.subheader("AI Air Quality Prediction & Monitoring")

# -----------------------------
# Load Model (cached)
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("model/model.pkl")

model = load_model()

# -----------------------------
# Cache AQI API data
# -----------------------------
@st.cache_data(ttl=600)
def get_real_aqi(city):
    url = f"https://api.waqi.info/feed/{city}/?token=0d7b964aed9d27f712884402c3f1b73dfe4fea47"
    response = requests.get(url, timeout=3)
    return response.json()

# -----------------------------
# AQI Prediction Section
# -----------------------------
st.header("🔮 Predict AQI")

with st.form("prediction_form"):

    pm25 = st.number_input("PM2.5", min_value=0.0)
    pm10 = st.number_input("PM10", min_value=0.0)
    no2 = st.number_input("NO2", min_value=0.0)

    green = st.slider("Green Cover (%)", 0, 100)
    traffic = st.slider("Traffic Density", 0, 100)
    industrial = st.slider("Industrial Emission", 0, 100)
    renewable = st.slider("Renewable Energy", 0, 100)

    submit = st.form_submit_button("Predict AQI")

if submit:

    data = np.array([[pm25, pm10, no2, green, traffic, industrial, renewable]])
    prediction = model.predict(data)[0]
    aqi = int(prediction)

    st.success(f"Predicted AQI: {aqi}")

    if aqi <= 50:
        st.success("Air Quality: Good 🌿")
    elif aqi <= 100:
        st.info("Air Quality: Moderate")
    elif aqi <= 150:
        st.warning("Air Quality: Unhealthy for Sensitive Groups")
    elif aqi <= 200:
        st.warning("Air Quality: Unhealthy")
    else:
        st.error("Air Quality: Hazardous 🚨")

# -----------------------------
# Real Time AQI Section
# -----------------------------
st.header("🌐 Real-Time AQI")

city = st.text_input("Enter City Name")

if st.button("Get Real-Time AQI"):

    try:
        data = get_real_aqi(city)

        if data["status"] == "ok":

            aqi = data["data"]["aqi"]
            st.success(f"Real-Time AQI in {city}: {aqi}")

            if aqi <= 50:
                st.success("Air Quality: Good 🌿")
            elif aqi <= 100:
                st.info("Air Quality: Moderate")
            elif aqi <= 150:
                st.warning("Air Quality: Unhealthy for Sensitive Groups")
            elif aqi <= 200:
                st.warning("Air Quality: Unhealthy")
            else:
                st.error("Air Quality: Hazardous 🚨")

        else:
            st.error("City not found")

    except:
        st.error("Error fetching data. Please try again.")
