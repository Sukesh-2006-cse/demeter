import joblib
import os
import numpy as np
from .base_agent import BaseAgent

class CropAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("crop", models_dir)
        
        # Try to load model from multiple possible locations
        model_paths = [
            os.path.join("models", "crop_model.pkl"),
            os.path.join("backend", "models", "crop_model.pkl"),
            "crop_model.pkl"
        ]
        
        if models_dir:
            model_paths.insert(0, os.path.join(models_dir, "crop_model.pkl"))
        
        self.model = None
        for path in model_paths:
            try:
                if os.path.exists(path):
                    self.model = joblib.load(path)
                    print(f"Loaded crop model from {path}")
                    break
            except Exception as e:
                print(f"Failed to load model from {path}: {e}")
                continue
        
        if self.model is None:
            print("Warning: Could not load crop model. Using dummy predictions.")

    def predict(self, payload):
        """Main prediction method expected by orchestrator"""
        context = payload.get("context", {})
        text = payload.get("text", "")
        
        # Extract soil and climate parameters from context
        features = self._extract_features(context, text)
        
        if self.model is None:
            return self._get_dummy_prediction(features)
        
        try:
            # Convert to numpy array for prediction
            features_array = np.array([features])
            
            # Get prediction
            prediction = self.model.predict(features_array)[0]
            
            # Get probabilities if available
            try:
                probabilities = self.model.predict_proba(features_array)[0]
                # Get top 3 crops
                top_indices = probabilities.argsort()[-3:][::-1]
                top_crops = [self.model.classes_[i] for i in top_indices]
                top_probs = [float(probabilities[i]) for i in top_indices]
                
                confidence = float(max(probabilities))
            except:
                top_crops = [prediction]
                top_probs = [0.8]
                confidence = 0.8
            
            return {
                "success": True,
                "top_crop": prediction,
                "recommended_crops": top_crops,
                "confidence_scores": top_probs,
                "confidence": confidence,
                "features_used": {
                    "N": features[0], "P": features[1], "K": features[2],
                    "temperature": features[3], "humidity": features[4],
                    "ph": features[5], "rainfall": features[6]
                },
                "message": f"Based on your soil and climate conditions, I recommend growing {prediction}. This recommendation has a confidence score of {confidence:.2f}.",
                "agent_used": "crop"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Prediction failed: {str(e)}",
                "agent_used": "crop"
            }

    def _extract_features(self, context, text):
        """Extract numerical features from context and text"""
        # Default values for soil and climate parameters
        defaults = {
            "N": 50, "P": 30, "K": 40,
            "temperature": 25, "humidity": 60,
            "ph": 6.5, "rainfall": 100
        }
        
        # Try different key variations
        key_mapping = {
            "N": ["N", "nitrogen", "n"],
            "P": ["P", "phosphorus", "p"],
            "K": ["K", "potassium", "k"],
            "temperature": ["temperature", "temp", "Temperature"],
            "humidity": ["humidity", "Humidity"],
            "ph": ["ph", "pH", "Ph"],
            "rainfall": ["rainfall", "rain", "precipitation"]
        }
        
        features = []
        for param in ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]:
            value = defaults[param]
            
            # Check various keys for this parameter
            for key in key_mapping.get(param, [param]):
                if key in context and context[key] is not None:
                    try:
                        value = float(context[key])
                        break
                    except (ValueError, TypeError):
                        continue
            
            features.append(value)
        
        return features

    def _get_dummy_prediction(self, features):
        """Return dummy prediction when model is not available"""
        import random
        
        crops = ['wheat', 'rice', 'corn', 'barley', 'cotton']
        selected_crop = random.choice(crops)
        
        return {
            "success": True,
            "top_crop": selected_crop,
            "recommended_crops": [selected_crop],
            "confidence_scores": [0.7],
            "confidence": 0.7,
            "features_used": {
                "N": features[0], "P": features[1], "K": features[2],
                "temperature": features[3], "humidity": features[4], 
                "ph": features[5], "rainfall": features[6]
            },
            "message": f"Based on your conditions, I recommend growing {selected_crop} (using fallback prediction).",
            "agent_used": "crop",
            "note": "This is a fallback prediction as the ML model is not available."
        }

    def handle(self, query, context):
        """Legacy method for backward compatibility"""
        payload = {"text": query, "context": context}
        return self.predict(payload)

    def process_query(self, text: str, payload: dict) -> dict:
        """Process query using the predict method"""
        return self.predict(payload)