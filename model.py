"""
RedShield AI - Crime Prediction Model
Run: python model.py
This trains a Random Forest model on FIR data and saves it.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

print("🔴 RedShield AI — Training Crime Prediction Model...")

# Load data
data = pd.read_csv("dataset/fir_data.csv")

# Encode crime types
le = LabelEncoder()
data["crime_encoded"] = le.fit_transform(data["crime_type"])

# Parse hour from time
data["hour"] = data["time"].apply(lambda t: int(t.split(":")[0]))

# Features: lat, lng, risk, hour
X = data[["latitude", "longitude", "risk", "hour"]]
y = data["crime_encoded"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
if len(X_test) > 0:
    y_pred = model.predict(X_test)
    print("\n📊 Model Performance:")
    print(classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0))

# Save
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/crime_model.pkl")
joblib.dump(le, "models/label_encoder.pkl")

print("✅ Model saved to models/crime_model.pkl")
print("✅ Encoder saved to models/label_encoder.pkl")
print("✅ Features used: latitude, longitude, risk, hour")


def predict_crime(latitude, longitude, risk, hour):
    """Load and use the trained model to predict crime type."""
    model = joblib.load("models/crime_model.pkl")
    le = joblib.load("models/label_encoder.pkl")
    pred = model.predict([[latitude, longitude, risk, hour]])
    return le.inverse_transform(pred)[0]


if __name__ == "__main__":
    # Demo prediction
    result = predict_crime(13.04, 80.23, 90, 22)
    print(f"\n🎯 Demo Prediction (lat=13.04, lng=80.23, risk=90, hour=22): {result}")
