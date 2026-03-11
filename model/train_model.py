import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("dataset/air_quality.csv")

# Features
X = df[['PM2_5','PM10','NO2','Green_Cover','Traffic_Density','Industrial_Emission','Renewable_Energy']]

# Target
y = df['AQI']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=200)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model/model.pkl")

print("Model trained successfully!")