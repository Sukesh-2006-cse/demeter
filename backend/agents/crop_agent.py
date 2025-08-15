import os, joblib, numpy as np
from .base_agent import BaseAgent

class CropAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("CropAdvisory", models_dir=models_dir)
        
        # Try multiple model paths for compatibility
        model_paths = [
            os.path.join(self.models_dir, "crop_model.pkl"),  # New trained model
            os.path.join(self.models_dir, "cloud", "crop_recommendation.pkl"),  # Backup location
            os.path.join(self.models_dir, "crop_recommendation.pkl")  # Legacy path
        ]
        
        self.model = None
        for path in model_paths:
            if os.path.exists(path):
                try:
                    self.model = joblib.load(path)
                    print(f"✅ Loaded crop model from: {path}")
                    break
                except Exception as e:
                    print(f"❌ Failed to load model from {path}: {e}")
                    continue
        
        if self.model is None:
            print("⚠️  No crop model found, using fallback heuristics")

    def predict(self, payload: dict) -> dict:
        """
        Predict crop recommendation based on soil and environmental conditions
        Expected features: N, P, K, temperature, humidity, ph, rainfall
        """
        ctx = payload.get("context", {})
        
        # Parse features with defaults (matching training data format)
        N = float(ctx.get("N", ctx.get("nitrogen", 90)))
        P = float(ctx.get("P", ctx.get("phosphorus", 42)))
        K = float(ctx.get("K", ctx.get("potassium", 43)))
        temperature = float(ctx.get("temperature", ctx.get("temp", 25.0)))
        humidity = float(ctx.get("humidity", 80.0))
        ph = float(ctx.get("ph", ctx.get("pH", 6.5)))
        rainfall = float(ctx.get("rainfall", ctx.get("rain", 200.0)))
        
        # Create feature array in the correct order: [N, P, K, temperature, humidity, ph, rainfall]
        X = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        
        if self.model:
            try:
                # Get prediction
                pred = self.model.predict(X)[0]
                
                # Get prediction probabilities for confidence
                probs = None
                confidence_score = 0.0
                try:
                    probs = self.model.predict_proba(X)[0]
                    confidence_score = float(np.max(probs))
                    probs = probs.tolist()
                except Exception:
                    probs = None
                    confidence_score = 0.8  # Default confidence for successful prediction
                
                return {
                    "top_crop": pred,
                    "recommended_crops": [pred],
                    "confidence": confidence_score,
                    "probabilities": probs,
                    "features_used": {
                        "N": N, "P": P, "K": K,
                        "temperature": temperature,
                        "humidity": humidity,
                        "ph": ph,
                        "rainfall": rainfall
                    },
                    "success": True,
                    "message": f"Based on your soil and climate conditions, I recommend growing {pred}."
                }
            except Exception as e:
                print(f"❌ Model prediction failed: {e}")
                return self._fallback_prediction(N, P, K, temperature, humidity, ph, rainfall)
        
        # Fallback heuristic when model is not available
        return self._fallback_prediction(N, P, K, temperature, humidity, ph, rainfall)

    def _fallback_prediction(self, N, P, K, temperature, humidity, ph, rainfall):
        """Fallback heuristic-based crop recommendation"""
        
        # Simple rule-based recommendations
        if rainfall > 150 and 5.0 <= ph <= 6.8 and humidity > 70:
            crop = "rice"
            confidence = 0.6
        elif temperature < 20 and rainfall < 100:
            crop = "wheat"
            confidence = 0.55
        elif 20 <= temperature <= 30 and 100 <= rainfall <= 200:
            crop = "maize"
            confidence = 0.5
        elif ph > 7.0 and rainfall < 80:
            crop = "cotton"
            confidence = 0.45
        else:
            crop = "maize"  # Default safe choice
            confidence = 0.4
        
        return {
            "top_crop": crop,
            "recommended_crops": [crop],
            "confidence": confidence,
            "probabilities": None,
            "features_used": {
                "N": N, "P": P, "K": K,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            },
            "success": True,
            "message": f"Based on basic heuristics, I recommend growing {crop}. For better accuracy, please ensure the ML model is properly loaded.",
            "fallback_used": True
        }

    def process_query(self, text: str, payload: dict) -> dict:
        """Enhanced query processing with parameter extraction from text"""
        
        # Try to extract parameters from text if not provided in context
        context = payload.get("context", {})
        parameters = payload.get("parameters", {})
        
        # Merge parameters into context
        for key, value in parameters.items():
            if key not in context and value is not None:
                context[key] = value
        
        # Update payload with enhanced context
        enhanced_payload = payload.copy()
        enhanced_payload["context"] = context
        
        return self.predict(enhanced_payload)

    def format_result_text(self, result, context):
        """Format the result into human-readable text"""
        crop = result.get("top_crop")
        confidence = result.get("confidence", 0)
        
        if isinstance(confidence, list) and len(confidence) > 0:
            confidence = max(confidence)
        
        confidence_text = f"{confidence:.1%}" if isinstance(confidence, (int, float)) else "N/A"
        
        base_text = f"Recommended crop: {crop}. Confidence: {confidence_text}."
        
        if result.get("fallback_used"):
            base_text += " (Using basic heuristics - ML model not available)"
        
        return base_text
