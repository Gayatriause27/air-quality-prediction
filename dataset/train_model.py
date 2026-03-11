import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("air_quality dataset.csv")

# Drop the Location column (not useful for ML)
df = df.drop(columns=["Location"])

# Encode City column
city_encoder = LabelEncoder()
df["City"] = city_encoder.fit_transform(df["City"])

# Encode target column
target_encoder = LabelEncoder()
df["Air_Quality"] = target_encoder.fit_transform(df["Air_Quality"])

# Features and Target
X = df.drop("Air_Quality", axis=1)
y = df["Air_Quality"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save model and encoders
joblib.dump(model, "air_quality_model.pkl")
joblib.dump(city_encoder, "city_encoder.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")

print("\nModel and encoders saved successfully.")