"""
Training script for crop recommendation model
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_crop_data():
    """Load crop recommendation dataset"""
    data_path = Path(__file__).parent.parent / "data" / "crop_dataset.csv"
    
    if not data_path.exists():
        logger.error(f"Dataset not found: {data_path}")
        return None
    
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Loaded dataset with {len(df)} samples")
        return df
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return None

def preprocess_data(df):
    """Preprocess the crop data"""
    # Features and target
    feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    target_column = 'label'
    
    X = df[feature_columns]
    y = df[target_column]
    
    return X, y

def train_model(X, y):
    """Train the crop recommendation model"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Initialize model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2
    )
    
    # Train model
    logger.info("Training model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    logger.info(f"Training accuracy: {train_score:.4f}")
    logger.info(f"Test accuracy: {test_score:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    logger.info(f"Cross-validation accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Predictions and detailed report
    y_pred = model.predict(X_test)
    logger.info("\nClassification Report:")
    logger.info(classification_report(y_test, y_pred))
    
    return model

def save_model(model, model_path):
    """Save the trained model"""
    try:
        # Ensure directory exists
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        logger.info(f"Model saved to {model_path}")
        
    except Exception as e:
        logger.error(f"Error saving model: {e}")

def main():
    """Main training pipeline"""
    logger.info("Starting crop recommendation model training...")
    
    # Load data
    df = load_crop_data()
    if df is None:
        return
    
    # Preprocess
    X, y = preprocess_data(df)
    
    # Train model
    model = train_model(X, y)
    
    # Save model
    model_path = Path(__file__).parent.parent / "models" / "cloud" / "crop_recommendation.pkl"
    save_model(model, model_path)
    
    logger.info("Training completed successfully!")

if __name__ == "__main__":
    main()