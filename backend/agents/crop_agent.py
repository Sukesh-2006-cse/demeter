import joblib
from .base_agent import BaseAgent

class CropAgent(BaseAgent):
    def __init__(self):
        self.model = joblib.load("backend/models/crop_model.pkl")

    def handle(self, query, context):
        """Handle crop recommendation - returns English results only"""
        # Extract features from context
        features = [[
            context.get("N", 50),
            context.get("P", 30),
            context.get("K", 40),
            context.get("temperature", 25),
            context.get("humidity", 60),
            context.get("ph", 6.5),
            context.get("rain", 100)
        ]]

        try:
            # Get prediction for top crop
            pred = self.model.predict(features)[0]
            
            # Get probabilities for top 3 crops
            try:
                probs = self.model.predict_proba(features)[0]
                # Get indices of top 3 probabilities
                top_3_indices = probs.argsort()[-3:][::-1]
                # Get corresponding crop names and confidence scores
                top_3_crops = [self.model.classes_[i] for i in top_3_indices]
                top_3_confidences = [float(probs[i]) for i in top_3_indices]
                
                # Create list of recommended crops with their confidence scores
                recommended_crops = []
                for i in range(len(top_3_crops)):
                    recommended_crops.append({
                        "crop": top_3_crops[i],
                        "confidence": top_3_confidences[i]
                    })
                
                confidence_score = float(max(probs))
            except Exception as e:
                print(f"Error getting probabilities in handle method: {e}")
                confidence_score = 0.8
                recommended_crops = [{"crop": pred, "confidence": confidence_score}]
                top_3_crops = [pred]
            
            return {
                "agent_used": "crop",
                "top_crop": pred,
                "original_crop": pred,
                "recommended_crops": top_3_crops,
                "detailed_recommendations": recommended_crops,
                "confidence": confidence_score
            }
        except Exception as e:
            print(f"❌ Model prediction failed in handle method: {e}")
            # Use fallback prediction if model fails
            fallback = self._fallback_prediction(
                context.get("N", 50),
                context.get("P", 30),
                context.get("K", 40),
                context.get("temperature", 25),
                context.get("humidity", 60),
                context.get("ph", 6.5),
                context.get("rain", 100)
            )
            return {
                "agent_used": "crop",
                "top_crop": fallback["top_crop"],
                "original_crop": fallback["top_crop"],
                "recommended_crops": fallback["recommended_crops"],
                "detailed_recommendations": fallback["detailed_recommendations"],
                "confidence": fallback["confidence"],
                "fallback_used": True
            }

    def predict(self, payload: dict) -> dict:
        """
        Predict crop recommendation based on soil and environmental conditions
        Returns results in English only - translation handled by multilingual pipeline
        """
        ctx = payload.get("context", {})
        
        # Parse features with defaults
        N = float(ctx.get("N", ctx.get("nitrogen", 90)))
        P = float(ctx.get("P", ctx.get("phosphorus", 42)))
        K = float(ctx.get("K", ctx.get("potassium", 43)))
        temperature = float(ctx.get("temperature", ctx.get("temp", 25.0)))
        humidity = float(ctx.get("humidity", 80.0))
        ph = float(ctx.get("ph", ctx.get("pH", 6.5)))
        rainfall = float(ctx.get("rainfall", ctx.get("rain", 200.0)))
        
        # Create feature array: [N, P, K, temperature, humidity, ph, rainfall]
        X = [[N, P, K, temperature, humidity, ph, rainfall]]
        
        try:
            # Get prediction for top crop
            pred = self.model.predict(X)[0]
            
            # Get probabilities for top 3 crops
            try:
                probs = self.model.predict_proba(X)[0]
                # Get indices of top 3 probabilities
                top_3_indices = probs.argsort()[-3:][::-1]
                # Get corresponding crop names and confidence scores
                top_3_crops = [self.model.classes_[i] for i in top_3_indices]
                top_3_confidences = [float(probs[i]) for i in top_3_indices]
                
                # Create list of recommended crops with their confidence scores
                recommended_crops = []
                for i in range(len(top_3_crops)):
                    recommended_crops.append({
                        "crop": top_3_crops[i],
                        "confidence": top_3_confidences[i]
                    })
                
                confidence_score = float(max(probs))
            except Exception as e:
                print(f"Error getting probabilities: {e}")
                confidence_score = 0.8
                recommended_crops = [{"crop": pred, "confidence": confidence_score}]
                top_3_crops = [pred]
            
            # Create message with top 3 recommendations
            message = "Based on your soil and climate conditions, I recommend growing:"  
            for i, crop_info in enumerate(recommended_crops):
                message += f"\n{i+1}. {crop_info['crop']} (Confidence: {crop_info['confidence']:.1%})"
            
            return {
                "agent_used": "crop",
                "top_crop": pred,
                "recommended_crops": top_3_crops,
                "detailed_recommendations": recommended_crops,
                "confidence": confidence_score,
                "features_used": {
                    "N": N, "P": P, "K": K,
                    "temperature": temperature,
                    "humidity": humidity,
                    "ph": ph,
                    "rainfall": rainfall
                },
                "success": True,
                "message": message
            }
        except Exception as e:
            print(f"❌ Model prediction failed: {e}")
            return self._fallback_prediction(N, P, K, temperature, humidity, ph, rainfall)

    def _fallback_prediction(self, N, P, K, temperature, humidity, ph, rainfall):
        """Fallback heuristic-based crop recommendation with top 3 crops"""
        
        # Define potential crops with their conditions and confidence scores
        potential_crops = [
            {"crop": "rice", "confidence": 0.6 if (rainfall > 150 and 5.0 <= ph <= 6.8 and humidity > 70) else 0.3},
            {"crop": "wheat", "confidence": 0.55 if (temperature < 20 and rainfall < 100) else 0.25},
            {"crop": "maize", "confidence": 0.5 if (20 <= temperature <= 30 and 100 <= rainfall <= 200) else 0.2},
            {"crop": "cotton", "confidence": 0.45 if (ph > 7.0 and rainfall < 80) else 0.15},
            {"crop": "chickpea", "confidence": 0.4 if (temperature > 25 and rainfall < 120) else 0.1},
            {"crop": "kidneybeans", "confidence": 0.35 if (humidity > 65 and 6.0 <= ph <= 7.5) else 0.05}
        ]
        
        # Sort crops by confidence score in descending order
        sorted_crops = sorted(potential_crops, key=lambda x: x["confidence"], reverse=True)
        
        # Get top 3 crops
        top_3_crops = sorted_crops[:3]
        top_crop = top_3_crops[0]["crop"]
        top_confidence = top_3_crops[0]["confidence"]
        
        # Create message with top 3 recommendations
        message = "Based on basic heuristics, I recommend growing:"  
        for i, crop_info in enumerate(top_3_crops):
            message += f"\n{i+1}. {crop_info['crop']} (Confidence: {crop_info['confidence']:.1%})"
        
        return {
            "agent_used": "crop",
            "top_crop": top_crop,
            "recommended_crops": [crop_info["crop"] for crop_info in top_3_crops],
            "detailed_recommendations": top_3_crops,
            "confidence": top_confidence,
            "features_used": {
                "N": N, "P": P, "K": K,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            },
            "success": True,
            "message": message,
            "fallback_used": True
        }

    def process_query(self, text: str, payload: dict) -> dict:
        """Process query using the predict method"""
        return self.predict(payload)

    def format_result_text(self, result, context):
        """Format result into readable text with top 3 recommendations"""
        recommended_crops = result.get("recommended_crops", [])
        detailed_recommendations = result.get("detailed_recommendations", [])
        
        if not recommended_crops:
            return "No crop recommendations available."
        
        # Start with a header
        base_text = "Top crop recommendations:\n"
        
        # If we have detailed recommendations with confidence scores
        if detailed_recommendations:
            for i, crop_info in enumerate(detailed_recommendations):
                crop_name = crop_info.get("crop")
                confidence = crop_info.get("confidence", 0)
                
                if isinstance(confidence, (int, float)):
                    confidence_text = f"{confidence:.1%}"
                else:
                    confidence_text = "N/A"
                    
                base_text += f"{i+1}. {crop_name} (Confidence: {confidence_text})\n"
        # Otherwise just list the crop names
        else:
            for i, crop in enumerate(recommended_crops[:3]):
                base_text += f"{i+1}. {crop}\n"
        
        if result.get("fallback_used"):
            base_text += "\n(Using basic heuristics due to model unavailability)"
        
        return base_text