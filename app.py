import streamlit as st
import joblib
import numpy as np
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="GreenAI AirSense", layout="centered")

st.title("🌍 GreenAI AirSense")
st.subheader("AI-Based Air Quality Prediction & Real-Time Monitoring")

# -------------------------------
# Load model (cached)
# -------------------------------

@st.cache_resource
def load_model():
    return joblib.load("model/model.pkl")

model = load_model()

# -------------------------------
# AI PREDICTION
# -------------------------------

st.header("🔮 Predict Air Quality (AI Model)")

pm25 = st.number_input("PM2.5", min_value=0.0)
pm10 = st.number_input("PM10", min_value=0.0)
no2 = st.number_input("NO2", min_value=0.0)

green_cover = st.slider("Green Cover (%)",0,100)
traffic = st.slider("Traffic Density",0,100)
industrial = st.slider("Industrial Emission",0,100)
renewable = st.slider("Renewable Energy Usage",0,100)

if st.button("Predict AQI"):

    data = np.array([[pm25, pm10, no2, green_cover, traffic, industrial, renewable]])
    prediction = model.predict(data)
    aqi = int(prediction[0])

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

    # Graph
    labels = ["PM2.5","PM10","NO2","Green","Traffic","Industrial","Renewable"]
    values = [pm25,pm10,no2,green_cover,traffic,industrial,renewable]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Pollution Factors")
    st.pyplot(fig)

# -------------------------------
# REAL TIME AQI
# -------------------------------

st.header("🌐 Real-Time Air Quality")

city = st.text_input("Enter City Name")

if st.button("Get Real-Time AQI"):

    try:
        url = f"https://api.waqi.info/feed/{city}/?token=0d7b964aed9d27f712884402c3f1b73dfe4fea47"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "ok":

            aqi = int(data["data"]["aqi"])
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
