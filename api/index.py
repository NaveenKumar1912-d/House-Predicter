import os
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

model_path = os.path.join(os.path.dirname(__file__), '..', 'model')
try:
    model = joblib.load(os.path.join(model_path, 'house_price_model.pkl'))
    scaler = joblib.load(os.path.join(model_path, 'scaler.pkl'))
    feature_cols = joblib.load(os.path.join(model_path, 'feature_cols.pkl'))
    model_name = joblib.load(os.path.join(model_path, 'model_name.pkl'))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def build_features(data):
    bedrooms = int(data.get('bedrooms', 0))
    bathrooms = int(data.get('bathrooms', 0))
    sqft = float(data.get('sqft', 0))
    year_built = int(data.get('year_built', 0))
    floors = int(data.get('floors', 0))
    garage = int(data.get('garage', 0))
    pool = int(data.get('pool', 0))
    location = int(data.get('location', 0))
    
    age = 2024 - year_built
    sqft_per_bed = sqft / max(bedrooms, 1)
    bath_bed = bathrooms / max(bedrooms, 1)
    amenity = garage + pool * 2
    new_const = 1 if age < 5 else 0
    luxury = 1 if sqft > 3000 and location == 2 else 0
    return [[bedrooms, bathrooms, sqft, age, floors, garage, pool,
             location, sqft_per_bed, bath_bed, amenity, new_const, luxury]]

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    data = request.json
    try:
        features = build_features(data)
        features_scaled = scaler.transform(features)
        price_lakhs = float(model.predict(features_scaled)[0])
        
        # Calculate EMI
        principal = price_lakhs * 100000
        rate_monthly = 8.5 / 100 / 12
        months = 240
        if rate_monthly > 0:
            emi = principal * rate_monthly * ((1 + rate_monthly)**months) / (((1 + rate_monthly)**months) - 1)
        else:
            emi = principal / months
            
        category = "Affordable" if price_lakhs < 30 else "Mid-Range" if price_lakhs < 80 else "Premium" if price_lakhs < 150 else "Luxury"
        
        return jsonify({
            "status": "success",
            "predicted_price": round(price_lakhs * 100000),
            "price_range": {
                "low": round(price_lakhs * 0.9 * 100000),
                "high": round(price_lakhs * 1.1 * 100000)
            },
            "currency": "INR",
            "category": category,
            "confidence": "High",
            "model_used": model_name,
            "emi_monthly": int(emi),
            "loan_tenure_years": 20,
            "interest_rate": 8.5
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
