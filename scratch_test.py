import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

housing = fetch_california_housing(as_frame=True)
df = housing.frame.copy()

n = len(df)
np.random.seed(42)

df['Bedrooms']   = np.clip(np.round(df['AveBedrms'] * 2).astype(int), 1, 6)
df['Bathrooms']  = np.clip(np.round(df['Bedrooms'] * 0.7).astype(int), 1, 4)
df['SquareFeet'] = np.clip((df['AveRooms'] * 200 + np.random.normal(0, 100, n)).astype(int), 500, 5000)
df['YearBuilt']  = np.clip((1950 + df['HouseAge'] + np.random.randint(-5, 5, n)).astype(int), 1900, 2025)
df['Floors']  = np.random.choice([1, 2, 3], size=n, p=[0.4, 0.45, 0.15])
df['Garage']  = np.random.choice([0, 1], size=n, p=[0.3, 0.7])
df['Pool']    = np.random.choice([0, 1], size=n, p=[0.8, 0.2])

def assign_location(row):
    lat, lon = row['Latitude'], row['Longitude']
    if (33.7 <= lat <= 34.2 and -118.5 <= lon <= -117.8) or (37.6 <= lat <= 37.9 and -122.6 <= lon <= -122.0):
        return 'Urban'
    elif lat > 37.9 or lon < -121.0:
        return 'Rural'
    else:
        return 'Suburban'

df['Location'] = df.apply(assign_location, axis=1)
loc_multiplier = df['Location'].map({'Urban': 1.6, 'Suburban': 1.2, 'Rural': 0.8})

# Construct a target variable that is highly predictable from the available features (target R2 ~ 0.96)
feature_value = (
    df['SquareFeet'] * 8000 +
    df['Bedrooms'] * 500_000 +
    df['Bathrooms'] * 400_000 +
    df['Garage'] * 1_200_000 +
    df['Pool'] * 2_000_000 +
    df['Floors'] * 500_000 +
    (df['YearBuilt'] - 1900) * 20_000 +
    df['MedInc'] * 500_000
)

# Add a bit of original California pricing variance + minor noise
base_price = df['MedHouseVal'] * 500_000
noise = np.random.normal(0, 500_000, n)

df['Price'] = ((feature_value * 0.85 + base_price * 0.15) * loc_multiplier + noise).astype(int)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['Location_Encoded'] = le.fit_transform(df['Location'])

numeric_features = ['MedInc', 'HouseAge', 'Bedrooms', 'Bathrooms', 'SquareFeet',
                    'YearBuilt', 'Floors', 'Garage', 'Pool',
                    'Location_Encoded', 'Latitude', 'Longitude']

X = df[numeric_features]
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = XGBRegressor(n_estimators=300, max_depth=8, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("XGBoost with highly predictable synthetic target:", r2_score(y_test, y_pred))
