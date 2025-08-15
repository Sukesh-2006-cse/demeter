"""
Training scripts for market price and yield prediction models
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import pickle
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_market_price_model():
    """Train market price prediction model"""
    logger.info("Training market price prediction model...")
    
    # Load data
    data_path = Path(__file__).parent.parent / "data" / "market_dataset.csv"
    
    if not data_path.exists():
        logger.warning(f"Market dataset not found: {data_path}")
        # Create dummy model for demonstration
        model = create_dummy_market_model()
    else:
        df = pd.read_csv(data_path)
        model = train_market_model_from_data(df)
    
    # Save model
    model_path = Path(__file__).parent.parent / "models" / "cloud" / "market_price.pkl"
    save_model(model, model_path, "market price")
    
    return model

def train_yield_prediction_model():
    """Train crop yield prediction model"""
    logger.info("Training yield prediction model...")
    
    # For demonstration, create a dummy model
    # In practice, this would load actual yield data
    model = create_dummy_yield_model()
    
    # Save model
    model_path = Path(__file__).parent.parent / "models" / "cloud" / "yield_model.pkl"
    save_model(model, model_path, "yield prediction")
    
    return model

def create_dummy_market_model():
    """Create a dummy market price model for demonstration"""
    # Create synthetic data
    np.random.seed(42)
    n_samples = 1000
    
    # Features: season, supply, demand, weather_index, historical_price
    X = np.random.randn(n_samples, 5)
    # Price influenced by supply/demand ratio and weather
    y = 100 + X[:, 1] * 20 - X[:, 2] * 15 + X[:, 3] * 10 + np.random.randn(n_samples) * 5
    
    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    logger.info("Created dummy market price model")
    return model

def create_dummy_yield_model():
    """Create a dummy yield prediction model for demonstration"""
    # Create synthetic data
    np.random.seed(42)
    n_samples = 800
    
    # Features: soil_quality, rainfall, temperature, fertilizer, seed_quality
    X = np.random.randn(n_samples, 5)
    # Yield influenced by all factors
    y = 5 + X[:, 0] * 1.5 + X[:, 1] * 1.2 + X[:, 2] * 0.8 + X[:, 3] * 1.0 + X[:, 4] * 0.9 + np.random.randn(n_samples) * 0.5
    y = np.maximum(y, 0)  # Ensure non-negative yields
    
    # Train model
    model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    logger.info("Created dummy yield prediction model")
    return model

def train_market_model_from_data(df):
    """Train market model from actual data"""
    # Prepare features
    feature_columns = ['supply', 'demand', 'weather_index', 'season_encoded', 'historical_avg']
    target_column = 'price'
    
    # Handle missing columns
    available_features = [col for col in feature_columns if col in df.columns]
    
    if not available_features or target_column not in df.columns:
        logger.warning("Required columns not found, creating dummy model")
        return create_dummy_market_model()
    
    X = df[available_features]
    y = df[target_column]
    
    # Handle missing values
    X = X.fillna(X.mean())
    y = y.fillna(y.mean())
    
    # Time series split for market data
    tscv = TimeSeriesSplit(n_splits=3)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Evaluate with time series cross-validation
    mse_scores = []
    for train_idx, test_idx in tscv.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mse_scores.append(mse)
    
    logger.info(f"Average MSE: {np.mean(mse_scores):.4f}")
    
    # Final training on all data
    model.fit(X, y)
    
    return model

def save_model(model, model_path, model_name):
    """Save trained model"""
    try:
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        logger.info(f"{model_name} model saved to {model_path}")
        
    except Exception as e:
        logger.error(f"Error saving {model_name} model: {e}")

def main():
    """Main training pipeline"""
    logger.info("Starting market and yield model training...")
    
    # Train both models
    market_model = train_market_price_model()
    yield_model = train_yield_prediction_model()
    
    logger.info("Training completed successfully!")

if __name__ == "__main__":
    main()