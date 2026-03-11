import streamlit as st
import joblib
import numpy as np
import requests

st.set_page_config(page_title="GreenAI AirSense", layout="centered")

st.title("🌍 GreenAI AirSense")
st.subheader("AI Air Quality Prediction & Monitoring")

# --------------------
# Load model only once
# --------------------

@st.cache_resource
def get_model():
    return joblib.load("model/model.pkl")

model = get_model()

# --------------------
# AI Prediction
# --------------------

st.header("🔮 Predict AQI")

pm25 = st.number_input("PM2.5",0.0)
pm10 = st.number_input("PM10",0.0)
no2 = st.number_input("NO2",0.0)

green = st.slider("Green Cover (%)",0,100)
traffic = st.slider("Traffic Density",0,100)
industrial = st.slider("Industrial Emission",0,100)
renewable = st.slider("Renewable Energy",0,100)

if st.button("Predict"):

    data = np.array([[pm25,pm10,no2,green,traffic,industrial,renewable]])

    pred = model.predict(data)[0]
    aqi = int(pred)

    st.success(f"AQI: {aqi}")

    if aqi <= 50:
        st.success("Good 🌿")
    elif aqi <= 100:
        st.info("Moderate")
    elif aqi <= 150:
        st.warning("Unhealthy for Sensitive Groups")
    elif aqi <= 200:
        st.warning("Unhealthy")
    else:
        st.error("Hazardous 🚨")

# --------------------
# Real Time AQI
# --------------------

st.header("🌐 Real-Time AQI")

city = st.text_input("City")

if st.button("Get AQI"):

    try:

        url = f"https://api.waqi.info/feed/{city}/?token=0d7b964aed9d27f712884402c3f1b73dfe4fea47"

        r = requests.get(url,timeout=3).json()

        if r["status"]=="ok":

            aqi = r["data"]["aqi"]
            st.success(f"{city} AQI: {aqi}")

        else:
            st.error("City not found")

    except:
        st.error("API Error")
