import streamlit as st
import joblib
import numpy as np
import pandas as pd
import requests
import altair as alt

st.set_page_config(page_title="GreenAI AirSense", layout="centered")

st.title("🌍 GreenAI AirSense")
st.subheader("AI-Based Air Quality Prediction & Real-Time Monitoring")

# -------------------------------
# Load model (cached)
# -------------------------------

@st.cache_resource
def load_model():
    model = joblib.load("model/model.pkl")
    return model

model = load_model()

# -------------------------------
# AI PREDICTION
# -------------------------------

st.header("🔮 Predict Air Quality (AI Model)")

with st.form("prediction_form"):

    pm25 = st.number_input("PM2.5", min_value=0.0)
    pm10 = st.number_input("PM10", min_value=0.0)
    no2 = st.number_input("NO2", min_value=0.0)

    green_cover = st.slider("Green Cover (%)",0,100)
    traffic = st.slider("Traffic Density",0,100)
    industrial = st.slider("Industrial Emission",0,100)
    renewable = st.slider("Renewable Energy Usage",0,100)

    predict_btn = st.form_submit_button("Predict AQI")

if predict_btn:

    with st.spinner("Predicting AQI..."):

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

    # Fast Altair Chart
    df = pd.DataFrame({
        "Factor": ["PM2.5","PM10","NO2","Green Cover","Traffic","Industrial","Renewable"],
        "Value": [pm25, pm10, no2, green_cover, traffic, industrial, renewable]
    })

    chart = alt.Chart(df).mark_bar().encode(
        x="Factor",
        y="Value",
        tooltip=["Factor","Value"]
    ).properties(
        title="Pollution Factors"
    )

    st.altair_chart(chart, use_container_width=True)

# -------------------------------
# REAL TIME AQI
# -------------------------------

st.header("🌐 Real-Time Air Quality")

city = st.text_input("Enter City Name")

if st.button("Get Real-Time AQI"):

    try:

        url = f"https://api.waqi.info/feed/{city}/?token=0d7b964aed9d27f712884402c3f1b73dfe4fea47"

        with st.spinner("Fetching real-time AQI..."):
            response = requests.get(url, timeout=5)
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
