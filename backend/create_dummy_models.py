#!/usr/bin/env python3
"""
Create dummy machine learning models for the Demeter project
This script creates mock models that can be used for testing and demonstration
"""

import os
import joblib
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyClassifier, DummyRegressor

# Create models directory
models_dir = "models"
saved_models_dir = "saved_models"
os.makedirs(models_dir, exist_ok=True)
os.makedirs(saved_models_dir, exist_ok=True)

print("Creating dummy ML models for Demeter...")

# 1. Crop Recommendation Model
print("1. Creating crop recommendation model...")
crop_classes = ['rice', 'wheat', 'corn', 'barley', 'sugarcane', 'cotton', 'jute', 'coconut', 
                'papaya', 'orange', 'apple', 'muskmelon', 'watermelon', 'grapes', 'mango', 
                'banana', 'pomegranate', 'lentil', 'blackgram', 'mungbean', 'mothbeans', 
                'pigeonpeas', 'kidneybeans', 'chickpea', 'coffee']

# Create dummy training data for crop model
# Features: N, P, K, temperature, humidity, ph, rainfall
np.random.seed(42)
X_crop = np.random.rand(1000, 7)
X_crop[:, 0] *= 100  # N (0-100)
X_crop[:, 1] *= 100  # P (0-100) 
X_crop[:, 2] *= 100  # K (0-100)
X_crop[:, 3] = X_crop[:, 3] * 20 + 15  # temperature (15-35°C)
X_crop[:, 4] *= 100  # humidity (0-100%)
X_crop[:, 5] = X_crop[:, 5] * 4 + 4  # ph (4-8)
X_crop[:, 6] *= 300  # rainfall (0-300mm)

y_crop = np.random.choice(crop_classes, 1000)

crop_model = RandomForestClassifier(n_estimators=10, random_state=42)
crop_model.fit(X_crop, y_crop)

# Save to both locations for compatibility
joblib.dump(crop_model, os.path.join(models_dir, "crop_model.pkl"))
if os.path.exists("backend"):
    os.makedirs("backend/models", exist_ok=True)
    joblib.dump(crop_model, os.path.join("backend", "models", "crop_model.pkl"))
else:
    # We're already in backend directory
    joblib.dump(crop_model, "crop_model.pkl")
print(f"   ✓ Saved crop model with {len(crop_classes)} crop classes")

# 2. Market Price Prediction Model
print("2. Creating market price prediction model...")
X_market = np.random.rand(1000, 5)  # Historical prices, demand, supply, season, weather
y_market = np.random.rand(1000) * 50 + 20  # Price range 20-70 rupees per kg

market_model = LinearRegression()
market_model.fit(X_market, y_market)

# Ensure reasonable predictions by clipping
class ClippedLinearRegression:
    def __init__(self, base_model, min_val=20, max_val=70):
        self.base_model = base_model
        self.min_val = min_val
        self.max_val = max_val
    
    def predict(self, X):
        predictions = self.base_model.predict(X)
        return np.clip(predictions, self.min_val, self.max_val)
    
    def __getattr__(self, name):
        return getattr(self.base_model, name)

market_model = ClippedLinearRegression(market_model)

joblib.dump(market_model, os.path.join(models_dir, "market_model.pkl"))
joblib.dump(market_model, os.path.join(saved_models_dir, "market_model.pkl"))
print("   ✓ Saved market price prediction model")

# 3. Yield Prediction Model
print("3. Creating yield prediction model...")
X_yield = np.random.rand(1000, 8)  # Soil, climate, crop type, area, fertilizer
y_yield = np.random.rand(1000) * 15 + 2  # Yield range 2-17 tons/hectare

yield_model = LinearRegression()
yield_model.fit(X_yield, y_yield)

# Ensure reasonable yield predictions
class ClippedYieldRegression:
    def __init__(self, base_model, min_val=2, max_val=17):
        self.base_model = base_model
        self.min_val = min_val
        self.max_val = max_val
    
    def predict(self, X):
        predictions = self.base_model.predict(X)
        return np.clip(predictions, self.min_val, self.max_val)
    
    def __getattr__(self, name):
        return getattr(self.base_model, name)

yield_model = ClippedYieldRegression(yield_model)

joblib.dump(yield_model, os.path.join(models_dir, "yield_model.pkl"))
joblib.dump(yield_model, os.path.join(saved_models_dir, "yield_model.pkl"))
print("   ✓ Saved yield prediction model")

# 4. Risk Assessment Model
print("4. Creating risk assessment model...")
risk_classes = ['low', 'medium', 'high']
X_risk = np.random.rand(1000, 6)  # Weather patterns, historical data, location
y_risk = np.random.choice(risk_classes, 1000)

risk_model = RandomForestClassifier(n_estimators=10, random_state=42)
risk_model.fit(X_risk, y_risk)

joblib.dump(risk_model, os.path.join(models_dir, "risk_model.pkl"))
joblib.dump(risk_model, os.path.join(saved_models_dir, "risk_model.pkl"))
print("   ✓ Saved risk assessment model")

# 5. Pest Detection Model
print("5. Creating pest detection model...")
pest_classes = ['armyworm', 'aphid', 'bollworm', 'cutworm', 'thrips', 'whitefly', 
                'brown_planthopper', 'stem_borer', 'leaf_miner', 'fruit_borer']

X_pest = np.random.rand(1000, 100)  # Image features (simplified)
y_pest = np.random.choice(pest_classes, 1000)

pest_model = RandomForestClassifier(n_estimators=10, random_state=42)
pest_model.fit(X_pest, y_pest)

joblib.dump(pest_model, os.path.join(models_dir, "pest_model.pkl"))
joblib.dump(pest_model, os.path.join(saved_models_dir, "pest_model.pkl"))
print("   ✓ Saved pest detection model")

# 6. Finance/Credit Model
print("6. Creating finance model...")
finance_classes = ['eligible', 'not_eligible', 'partial_eligible']
X_finance = np.random.rand(1000, 5)  # Income, land size, credit history, crop type, location
y_finance = np.random.choice(finance_classes, 1000)

finance_model = RandomForestClassifier(n_estimators=10, random_state=42)
finance_model.fit(X_finance, y_finance)

joblib.dump(finance_model, os.path.join(models_dir, "finance_model.pkl"))
joblib.dump(finance_model, os.path.join(saved_models_dir, "finance_model.pkl"))
print("   ✓ Saved finance model")

# Create model metadata
print("7. Creating model metadata...")
model_metadata = {
    "crop_model": {
        "features": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"],
        "classes": crop_classes,
        "description": "Random Forest model for crop recommendation based on soil and climate"
    },
    "market_model": {
        "features": ["historical_price", "demand", "supply", "season", "weather_score"],
        "description": "Linear regression model for market price prediction"
    },
    "yield_model": {
        "features": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "area"],
        "description": "Linear regression model for crop yield prediction"
    },
    "risk_model": {
        "features": ["temperature", "humidity", "rainfall", "wind_speed", "pressure", "location_risk"],
        "classes": risk_classes,
        "description": "Random Forest model for agricultural risk assessment"
    },
    "pest_model": {
        "features": ["image_features"],
        "classes": pest_classes,
        "description": "Random Forest model for pest detection from images"
    },
    "finance_model": {
        "features": ["income", "land_size", "credit_score", "crop_value", "location_score"],
        "classes": finance_classes,
        "description": "Random Forest model for agricultural finance eligibility"
    }
}

with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
    import json
    json.dump(model_metadata, f, indent=2)

print("   ✓ Saved model metadata")

print("\n✅ All dummy models created successfully!")
print(f"Models saved to: {models_dir}/ and {saved_models_dir}/")
print("\nNote: These are dummy models for development/testing.")
print("Replace with real trained models for production use.")