"""
Training script for weather risk assessment model
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_weather_risk_data():
    """Create synthetic weather risk data for training"""
    np.random.seed(42)
    n_samples = 2000
    
    # Weather features
    temperature = np.random.normal(25, 10, n_samples)  # Celsius
    humidity = np.random.uniform(20, 100, n_samples)   # Percentage
    rainfall = np.random.exponential(5, n_samples)     # mm
    wind_speed = np.random.gamma(2, 3, n_samples)      # m/s
    pressure = np.random.normal(1013, 20, n_samples)   # hPa
    
    # Create risk labels based on weather conditions
    risk_scores = []
    
    for i in range(n_samples):
        risk = 0
        
        # Temperature risk
        if temperature[i] > 40 or temperature[i] < 0:
            risk += 0.3
        elif temperature[i] > 35 or temperature[i] < 5:
            risk += 0.2
        
        # Humidity risk
        if humidity[i] > 90:
            risk += 0.2
        elif humidity[i] < 30:
            risk += 0.15
        
        # Rainfall risk
        if rainfall[i] > 50:  # Heavy rain
            risk += 0.25
        elif rainfall[i] < 1:  # Drought
            risk += 0.3
        
        # Wind risk
        if wind_speed[i] > 15:  # Strong wind
            risk += 0.2
        
        # Pressure risk
        if pressure[i] < 980:  # Low pressure (storms)
            risk += 0.15
        
        risk_scores.append(min(risk, 1.0))  # Cap at 1.0
    
    # Convert to risk categories
    risk_categories = []
    for score in risk_scores:
        if score >= 0.7:
            risk_categories.append('high')
        elif score >= 0.4:
            risk_categories.append('medium')
        else:
            risk_categories.append('low')
    
    # Create DataFrame
    df = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'rainfall': rainfall,
        'wind_speed': wind_speed,
        'pressure': pressure,
        'risk_score': risk_scores,
        'risk_category': risk_categories
    })
    
    return df

def train_weather_risk_model():
    """Train weather risk assessment model"""
    logger.info("Creating synthetic weather risk data...")
    df = create_weather_risk_data()
    
    # Features and target
    feature_columns = ['temperature', 'humidity', 'rainfall', 'wind_speed', 'pressure']
    target_column = 'risk_category'
    
    X = df[feature_columns]
    y = df[target_column]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    logger.info("Training weather risk model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    logger.info(f"Training accuracy: {train_score:.4f}")
    logger.info(f"Test accuracy: {test_score:.4f}")
    
    # Detailed evaluation
    y_pred = model.predict(X_test_scaled)
    logger.info("\nClassification Report:")
    logger.info(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    logger.info("\nFeature Importance:")
    logger.info(feature_importance)
    
    # Package model with scaler
    model_package = {
        'model': model,
        'scaler': scaler,
        'feature_columns': feature_columns,
        'risk_categories': ['low', 'medium', 'high']
    }
    
    return model_package

def save_model(model_package, model_path):
    """Save the trained model package"""
    try:
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_package, f)
        
        logger.info(f"Weather risk model saved to {model_path}")
        
    except Exception as e:
        logger.error(f"Error saving model: {e}")

def main():
    """Main training pipeline"""
    logger.info("Starting weather risk model training...")
    
    # Train model
    model_package = train_weather_risk_model()
    
    # Save model
    model_path = Path(__file__).parent.parent / "models" / "cloud" / "weather_risk.pkl"
    save_model(model_package, model_path)
    
    logger.info("Weather risk model training completed successfully!")

if __name__ == "__main__":
    main()