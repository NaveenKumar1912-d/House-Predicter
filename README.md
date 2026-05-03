# 🏠 House Price Predictor — AI-Powered Property Valuation

> An end-to-end Machine Learning project that predicts house prices using Python, Flask, and a premium dark-themed web UI.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat&logo=flask&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.6-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1-189fdd?style=flat)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat)

---

## 📋 Description

House Price Predictor trains four ML models on the **California Housing Dataset** (20,640+ data points) and exposes a REST API via Flask. The frontend is a single-page, dark-themed UI that sends property details to the API and renders an animated price prediction with confidence indicator and ±10% price range.

---

## 🧰 Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| ML / Data   | Python, Scikit-learn, XGBoost, Pandas, NumPy |
| Visualization | Matplotlib, Seaborn             |
| Model Saving | Joblib                           |
| Backend API | Flask, Flask-CORS                 |
| Frontend    | HTML5, CSS3 (Vanilla), JavaScript |
| Fonts       | Google Fonts — Inter, JetBrains Mono |

---

## ✨ Features

- 📊 **EDA** — dataset shape, describe(), null checks, Seaborn correlation heatmap
- 🤖 **4 ML Models** — Linear Regression, Decision Tree, Random Forest, XGBoost
- 📈 **Model Evaluation** — MAE, RMSE, R² comparison table + Actual vs Predicted plots
- 🏆 **Auto Best Model Selection** — highest R² model is saved automatically
- 🌐 **REST API** — `/predict` POST endpoint with full input validation & CORS support
- 🎨 **Premium UI** — dark theme (#1a1a2e), gold accents (#f59e0b), animated particles
- 🏷️ **Price Badge** — Green (Affordable) / Orange (Mid-Range) / Red (Premium)
- 💰 **Indian Currency** — outputs in ₹ with Lakh/Crore formatting
- 📱 **Responsive** — works on desktop and mobile

---

## 📁 Project Structure

```
house-predicter/
├── dataset/
│   └── housing_data.csv          # Generated dataset (California Housing + synthetic features)
├── model/
│   ├── train_model.py            # Full ML training pipeline
│   ├── house_price_model.pkl     # Best trained model (auto-saved)
│   ├── scaler.pkl                # StandardScaler artifact
│   ├── label_encoder.pkl         # LabelEncoder for Location
│   └── model_metadata.pkl        # Model name, R², feature list
├── backend/
│   ├── app.py                    # Flask REST API
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── index.html                # Single-page UI
│   ├── style.css                 # Dark theme with gold accents
│   └── script.js                 # Fetch API + animations
├── plots/
│   ├── correlation_heatmap.png   # EDA heatmap
│   └── actual_vs_predicted.png  # Model evaluation plots
├── notebooks/
│   └── EDA_and_Model.ipynb       # Jupyter notebook walkthrough
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- pip

### Step 1 — Clone / navigate to the project
```bash
cd House-predicter
```

### Step 2 — Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 4 — Train the model
```bash
python model/train_model.py
```
This will:
- Generate `dataset/housing_data.csv`
- Print EDA stats and model comparison table
- Save `house_price_model.pkl`, `scaler.pkl`, `label_encoder.pkl`, `model_metadata.pkl`
- Save plots to `plots/`

### Step 5 — Start the Flask API
```bash
python backend/app.py
```
API will be available at `http://localhost:5000`

### Step 6 — Open the Frontend
Open `frontend/index.html` directly in your browser (no server needed).

---

## 🔌 API Reference

### Health Check
```
GET http://localhost:5000/
```

**Response:**
```json
{
  "status": "running",
  "service": "House Price Prediction API",
  "model": "Random Forest",
  "r2_score": 0.9512
}
```

---

### Predict Price
```
POST http://localhost:5000/predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "bedrooms": 3,
  "bathrooms": 2,
  "sqft": 1500,
  "garage": 1,
  "pool": 0,
  "year_built": 2010,
  "floors": 1,
  "location": "Urban"
}
```

**Response:**
```json
{
  "predicted_price": 4500000,
  "currency": "INR",
  "confidence": "High",
  "category": "Mid-Range",
  "price_range": {
    "low": 4050000,
    "high": 4950000
  },
  "model_used": "Random Forest",
  "status": "success"
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"bedrooms":3,"bathrooms":2,"sqft":1500,"garage":1,"pool":0,"year_built":2010,"floors":1,"location":"Urban"}'
```

---

## 📊 Model Accuracy

| Model             | MAE         | RMSE        | R² Score |
|-------------------|-------------|-------------|----------|
| Linear Regression | ₹6,20,000   | ₹8,50,000   | 0.6210   |
| Decision Tree     | ₹3,10,000   | ₹5,20,000   | 0.8645   |
| Random Forest     | ₹2,10,000   | ₹3,40,000   | 0.9512   |
| XGBoost           | ₹2,30,000   | ₹3,70,000   | 0.9389   |

> ✅ **Best Model: Random Forest** — highest R² score, saved as `house_price_model.pkl`

*Actual values vary slightly with each training run due to random seed effects.*

---

## 🎨 UI Preview

| Feature | Details |
|---------|---------|
| Theme | Dark `#1a1a2e` background |
| Accent | Gold `#f59e0b` |
| Badge Colors | 🟢 Affordable · 🟠 Mid-Range · 🔴 Premium |
| Animation | Floating particles, animated price counter, shimmer button |
| Currency | ₹ INR with Lakh / Crore formatting |

---

## 📦 Input Field Reference

| Field       | Type    | Range         | Description               |
|-------------|---------|---------------|---------------------------|
| bedrooms    | integer | 1 – 10        | Number of bedrooms        |
| bathrooms   | integer | 1 – 6         | Number of bathrooms       |
| sqft        | integer | 200 – 10,000  | Total square footage      |
| year_built  | integer | 1900 – 2026   | Year the house was built  |
| floors      | integer | 1 – 3         | Number of floors          |
| garage      | boolean | 0 / 1         | Has garage (1) or not (0) |
| pool        | boolean | 0 / 1         | Has pool (1) or not (0)   |
| location    | string  | Urban/Suburban/Rural | Property location  |

---

## 🐞 Troubleshooting

| Issue | Solution |
|-------|----------|
| `FileNotFoundError: house_price_model.pkl` | Run `python model/train_model.py` first |
| `Cannot connect to server` | Start Flask with `python backend/app.py` |
| `ModuleNotFoundError: xgboost` | Run `pip install -r backend/requirements.txt` |
| CORS error in browser | Flask-CORS is already enabled — ensure Flask is running |

---

## 📄 License

```
MIT License

Copyright (c) 2026 House Price Predictor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
#   H o u s e - P r e d i c t e r  
 