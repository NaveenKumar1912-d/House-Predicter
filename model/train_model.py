import numpy as np
import pandas as pd
import random
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
import os

# 1. Generate Synthetic Data
np.random.seed(42)
random.seed(42)

n_samples = 20000
data = []
for _ in range(n_samples):
    bedrooms = random.choices([1, 2, 3, 4, 5, 6], weights=[5, 25, 35, 20, 10, 5])[0]
    bathrooms = np.clip(bedrooms - random.randint(0, 1), 1, 5)
    sqft = bedrooms * random.uniform(350, 600) + np.random.uniform(-100, 100)
    year_built = random.randint(1970, 2024)
    age = 2024 - year_built
    floors = random.choice([1, 2, 3, 4])
    garage = random.choice([0, 1])
    pool = random.choices([0, 1], weights=[75, 25])[0]
    location = random.choice([0, 1, 2])
    loc_mult = 1.0 if location == 0 else 1.3 if location == 1 else 1.8
    
    price_calc = (sqft * 3.2 * loc_mult + bedrooms * 180000 + bathrooms * 120000 +
                  floors * 80000 + garage * 250000 + pool * 500000 - age * 15000 + random.uniform(0, 200000)) / 100000
    price_lakhs = np.clip(price_calc, 8, 500)
    
    data.append([bedrooms, bathrooms, sqft, year_built, age, floors, garage, pool, location, price_lakhs])

df = pd.DataFrame(data, columns=['bedrooms', 'bathrooms', 'sqft', 'year_built', 'age', 'floors', 'garage', 'pool', 'location', 'price_lakhs'])

# 2. Feature Engineering
df['sqft_per_bed'] = df['sqft'] / df['bedrooms']
df['bath_bed_ratio'] = df['bathrooms'] / df['bedrooms']
df['amenity_score'] = df['garage'] + df['pool'] * 2
df['new_construction'] = (df['age'] < 5).astype(int)
df['luxury_flag'] = ((df['sqft'] > 3000) & (df['location'] == 2)).astype(int)

feature_cols = ['bedrooms', 'bathrooms', 'sqft', 'age', 'floors', 'garage', 'pool', 'location', 
                'sqft_per_bed', 'bath_bed_ratio', 'amenity_score', 'new_construction', 'luxury_flag']

X = df[feature_cols]
y = df['price_lakhs']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Train Models
models = {
    "GradientBoosting": GradientBoostingRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42),
    "RandomForest": RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42),
    "Ridge": Ridge(alpha=1.0)
}

best_model = None
best_r2 = -float('inf')
best_name = ""

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    print(f"{name} R2 Score: {r2:.4f}")
    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_name = name

print(f"\nTarget accuracy check (R2 > 0.80): {best_r2 > 0.80} (Best: {best_r2:.4f} with {best_name})")

# 5. Save artifacts
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'model'), exist_ok=True)
model_dir = os.path.join(os.path.dirname(__file__), '..', 'model')
joblib.dump(best_model, os.path.join(model_dir, "house_price_model.pkl"))
joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))
joblib.dump(feature_cols, os.path.join(model_dir, "feature_cols.pkl"))
joblib.dump(best_name, os.path.join(model_dir, "model_name.pkl"))
print("Saved models and artifacts.")

# 6. Sanity check
def predict_sample(bedrooms, bathrooms, sqft, year_built, floors, garage, pool, location):
    age = 2024 - year_built
    sqft_per_bed = sqft / max(bedrooms, 1)
    bath_bed_ratio = bathrooms / max(bedrooms, 1)
    amenity_score = garage + pool * 2
    new_construction = 1 if age < 5 else 0
    luxury_flag = 1 if sqft > 3000 and location == 2 else 0
    
    features = [[bedrooms, bathrooms, sqft, age, floors, garage, pool, location,
                 sqft_per_bed, bath_bed_ratio, amenity_score, new_construction, luxury_flag]]
    features_scaled = scaler.transform(features)
    return best_model.predict(features_scaled)[0]

print("\nSanity Check:")
p1 = predict_sample(1, 1, 500, 2020, 1, 0, 0, 0)
print(f"1BHK Rural  500sqft  2020 -> ~Rs {p1:.1f}L")
p2 = predict_sample(3, 2, 1500, 2015, 2, 1, 0, 1)
print(f"3BHK Suburb 1500sqft 2015 -> ~Rs {p2:.1f}L")
p3 = predict_sample(5, 5, 4000, 2022, 3, 1, 1, 2)
print(f"5BHK Urban  4000sqft 2022 -> ~Rs {p3:.1f}L")
