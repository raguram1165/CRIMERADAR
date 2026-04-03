# 🛡️ RedShield AI — Smart Policing Platform

> Hackathon-grade AI-powered public safety platform built with Flask, Leaflet, Chart.js, OpenCV & scikit-learn.

---

## 🎯 Features

| Feature | File | Status |
|---------|------|--------|
| Crime Heatmap | `app.py` + `index.html` | ✅ |
| AI Crime Prediction | `model.py` | ✅ |
| Smart Patrol Routing | `route_optimizer.py` | ✅ |
| Women SOS Emergency | `index.html` | ✅ |
| CCTV AI Detection | `cctv_detection.py` | ✅ |
| Accident Blackspots | `app.py` | ✅ |
| Crime Dashboard | `index.html` | ✅ |
| Risk Score Engine | `app.py` `/predict` | ✅ |
| FIR Registration | `app.py` + `index.html` | ✅ |
| AI Chatbot | `chatbot.py` + `index.html` | ✅ |

---

## 🚀 Quick Start

### Step 1 — Install dependencies
```bash
pip install flask pandas scikit-learn opencv-python networkx joblib numpy
```

### Step 2 — Train the AI model
```bash
python model.py
```

### Step 3 — Run the main dashboard
```bash
python app.py
```
Open: http://localhost:5000

### Step 4 (Optional) — Run CCTV detection
```bash
python cctv_detection.py
```

### Step 5 (Optional) — Run patrol optimizer standalone
```bash
python route_optimizer.py
```

### Step 6 (Optional) — Run chatbot in terminal
```bash
python chatbot.py
```

---

## 📁 Folder Structure

```
redshield-ai-smart-policing/
│
├── app.py                  ← Flask backend (main server)
├── model.py                ← AI crime prediction (Random Forest)
├── cctv_detection.py       ← CCTV with motion detection
├── route_optimizer.py      ← Smart patrol route (NetworkX/Dijkstra)
├── chatbot.py              ← AI chatbot assistant
├── requirements.txt        ← Python packages
├── README.md               ← This file
│
├── dataset/
│   ├── fir_data.csv        ← Crime FIR records
│   ├── accident_data.csv   ← Accident blackspot data
│   └── women_safety.csv    ← Women safety zone data
│
├── templates/
│   └── index.html          ← Full dashboard UI
│
├── static/
│   └── style.css           ← (Additional styles if needed)
│
└── models/
    ├── crime_model.pkl     ← Trained model (after running model.py)
    └── label_encoder.pkl   ← Encoder (after running model.py)
```

---

## 🧠 AI Features Explained

### Crime Prediction (`/predict`)
- Click any location on the map
- AI calculates risk score based on nearby FIR history
- Returns: risk score, alert level (LOW/MEDIUM/HIGH), predicted crime type

### Smart Patrol Route
- Greedy nearest-neighbor algorithm on high-risk zones
- Minimizes patrol distance while covering all hotspots
- Real-time update with every new FIR

### CCTV Detection
- Background subtraction (MOG2) for motion detection
- Auto-saves alert snapshots
- Controls: `Q` quit | `S` snapshot | `R` reset background model

---

## 🏆 Hackathon Demo Flow

1. Show live **crime heatmap** — red/orange clusters
2. Click map → **AI prediction** popup appears
3. Click **Patrol Route** → route draws on map
4. Register a new **FIR** → new marker appears instantly
5. Press **SOS** → alert banner flashes
6. Show **CCTV** window (run in separate terminal)
7. Demo the **AI Chatbot** in right panel

---

## 📞 Emergency Numbers (Chennai)
- Police: 100
- Ambulance: 108
- Fire: 101
- Women Helpline: 181
- Child Helpline: 1098
- Cyber Crime: 1930
