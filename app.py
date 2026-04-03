from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import os

app = Flask(__name__)

FIR_FILE = "dataset/fir_data.csv"
ACCIDENT_FILE = "dataset/accident_data.csv"
WOMEN_FILE = "dataset/women_safety.csv"


def load_fir():
    return pd.read_csv(FIR_FILE)


def load_accidents():
    return pd.read_csv(ACCIDENT_FILE)


def load_women():
    return pd.read_csv(WOMEN_FILE)


@app.route("/")
def home():
    crimes = load_fir().to_dict(orient="records")
    accidents = load_accidents().to_dict(orient="records")
    women_zones = load_women().to_dict(orient="records")

    # Stats
    df = load_fir()
    total_crimes = len(df)
    high_risk = len(df[df["risk"] >= 85])
    crime_types = df["crime_type"].value_counts().to_dict()
    locations = df["location"].value_counts().head(5).to_dict()

    return render_template(
        "index.html",
        crimes=crimes,
        accidents=accidents,
        women_zones=women_zones,
        total_crimes=total_crimes,
        high_risk=high_risk,
        crime_types=json.dumps(crime_types),
        locations=json.dumps(locations),
    )


@app.route("/add_fir", methods=["POST"])
def add_fir():
    crime_type = request.form["crime_type"]
    location = request.form["location"]
    latitude = float(request.form["latitude"])
    longitude = float(request.form["longitude"])
    date = request.form["date"]
    time = request.form["time"]

    risk = 95 if crime_type.lower() in ["robbery", "assault", "harassment"] else 75

    new_row = pd.DataFrame([{
        "crime_type": crime_type,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "date": date,
        "time": time,
        "risk": risk
    }])

    data = load_fir()
    data = pd.concat([data, new_row], ignore_index=True)
    data.to_csv(FIR_FILE, index=False)

    return jsonify({"status": "success", "message": "FIR registered successfully", "risk": risk})


@app.route("/predict", methods=["POST"])
def predict():
    """AI crime prediction endpoint"""
    lat = float(request.json.get("latitude", 13.0827))
    lng = float(request.json.get("longitude", 80.2707))

    df = load_fir()
    # Simple risk scoring based on nearby crimes
    df["dist"] = ((df["latitude"] - lat)**2 + (df["longitude"] - lng)**2)**0.5
    nearby = df[df["dist"] < 0.05]

    if len(nearby) > 0:
        avg_risk = nearby["risk"].mean()
        top_crime = nearby["crime_type"].mode()[0]
        prediction = {
            "risk_score": round(avg_risk, 1),
            "predicted_crime": top_crime,
            "nearby_incidents": len(nearby),
            "alert_level": "HIGH" if avg_risk > 85 else "MEDIUM" if avg_risk > 70 else "LOW"
        }
    else:
        prediction = {
            "risk_score": 30,
            "predicted_crime": "None",
            "nearby_incidents": 0,
            "alert_level": "LOW"
        }

    return jsonify(prediction)


@app.route("/patrol_route")
def patrol_route():
    """Optimized patrol route using greedy nearest-neighbor"""
    df = load_fir()
    high_risk = df[df["risk"] >= 85].copy()

    # Start from police station (central Chennai)
    station = {"name": "Chennai Central Police Station", "lat": 13.0827, "lng": 80.2707}
    route = [station]
    visited = set()

    remaining = high_risk.to_dict(orient="records")

    current_lat, current_lng = station["lat"], station["lng"]

    while remaining:
        # Find nearest unvisited hotspot
        min_dist = float("inf")
        nearest = None
        nearest_idx = None

        for i, point in enumerate(remaining):
            dist = ((point["latitude"] - current_lat)**2 + (point["longitude"] - current_lng)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                nearest = point
                nearest_idx = i

        if nearest:
            route.append({
                "name": nearest["location"],
                "lat": nearest["latitude"],
                "lng": nearest["longitude"],
                "risk": nearest["risk"],
                "crime": nearest["crime_type"]
            })
            current_lat = nearest["latitude"]
            current_lng = nearest["longitude"]
            remaining.pop(nearest_idx)

    # Return to station
    route.append(station)

    return jsonify({"route": route, "stops": len(route)})


@app.route("/api/stats")
def api_stats():
    df = load_fir()
    return jsonify({
        "total": len(df),
        "high_risk": len(df[df["risk"] >= 85]),
        "by_type": df["crime_type"].value_counts().to_dict(),
        "by_location": df["location"].value_counts().head(5).to_dict(),
        "avg_risk": round(df["risk"].mean(), 1)
    })


if __name__ == "__main__":
    app.run(debug=True)
