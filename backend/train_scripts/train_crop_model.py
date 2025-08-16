"""
Training script for crop recommendation model
Optimized for >85% accuracy
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from pathlib import Path
import os

def main():
    # 1. Load dataset
    data_path = Path(__file__).parent.parent / "data" / "Crop_recommendation.csv"
    df = pd.read_csv(data_path)
    
    print(f"Dataset loaded: {len(df)} samples, {len(df.columns)} features")
    print(f"Unique crops: {df['label'].nunique()}")
    
    # 2. Split features & target
    X = df.drop("label", axis=1)  # features
    y = df["label"]               # target
    
    # 3. Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Train model with optimized parameters for >85% accuracy
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        max_depth=15,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features='sqrt',
        bootstrap=True
    )
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    # 5. Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Training complete. Accuracy: {accuracy:.2%}")
    
    # Ensure we meet the >85% requirement
    if accuracy < 0.85:
        print(f"⚠️  Warning: Accuracy {accuracy:.2%} is below 85% target")
    else:
        print(f"🎯 Target achieved! Accuracy {accuracy:.2%} exceeds 85%")
    
    # 6. Save model
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / "crop_model.pkl"
    joblib.dump(model, model_path)
    print(f"📂 Model saved to {model_path}")
    
    # Also save to cloud models directory for consistency
    cloud_models_dir = models_dir / "cloud"
    cloud_models_dir.mkdir(exist_ok=True)
    cloud_model_path = cloud_models_dir / "crop_recommendation.pkl"
    joblib.dump(model, cloud_model_path)
    print(f"📂 Model also saved to {cloud_model_path}")
    
    # 7. Save accuracy log
    metrics_path = models_dir / "crop_model_metrics.txt"
    with open(metrics_path, "w") as f:
        f.write(f"Crop Model Accuracy: {accuracy:.4f}\n")
        f.write(f"Training samples: {len(X_train)}\n")
        f.write(f"Test samples: {len(X_test)}\n")
        f.write(f"Number of features: {X.shape[1]}\n")
        f.write(f"Number of classes: {y.nunique()}\n")
        f.write(f"Model parameters: n_estimators=200, max_depth=15\n")
    
    print(f"📊 Metrics saved to {metrics_path}")
    
    # Feature importance analysis
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🔍 Feature Importance:")
    for _, row in feature_importance.iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")

if __name__ == "__main__":
    main()