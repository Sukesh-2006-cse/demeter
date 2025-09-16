import os
import joblib
import numpy as np
from .base_agent import BaseAgent

class RiskAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("risk", models_dir=models_dir)
        
        # Try to load risk model from multiple locations
        model_paths = [
            os.path.join("models", "risk_model.pkl"),
            os.path.join(models_dir or "", "risk_model.pkl"),
        ]
        
        self.model = None
        for path in model_paths:
            if os.path.exists(path):
                try:
                    self.model = joblib.load(path)
                    print(f"Loaded risk model from {path}")
                    break
                except Exception as e:
                    print(f"Failed to load risk model from {path}: {e}")
        
        if self.model is None:
            print("Warning: Could not load risk model. Using heuristic predictions.")

    def predict(self, payload: dict) -> dict:
        """Main prediction method for agricultural risk assessment"""
        context = payload.get("context", {})
        text = payload.get("text", "")
        
        try:
            # Extract parameters from context
            location = context.get("location", "unknown")
            crop = context.get("crop", "general crops")
            
            # Weather data
            weather_data = context.get("weather_data", {})
            temperature = float(weather_data.get("temperature", context.get("temperature", context.get("temp", 25))))
            humidity = float(weather_data.get("humidity", context.get("humidity", context.get("hum", 60))))
            rainfall = float(weather_data.get("rainfall", context.get("rainfall", context.get("rain", context.get("recent_rain", 100)))))
            wind_speed = float(weather_data.get("wind_speed", context.get("wind_speed", 10)))
            pressure = float(weather_data.get("pressure", context.get("pressure", 1013)))
            
            time_period = context.get("time_period", "this season")
            
            if self.model:
                # Features: temperature, humidity, rainfall, wind_speed, pressure, location_risk
                location_risk = self._get_location_risk_score(location)
                features = np.array([[temperature, humidity, rainfall, wind_speed, pressure, location_risk]])
                
                risk_prediction = self.model.predict(features)[0]
                
                # Get probabilities if available
                try:
                    probabilities = self.model.predict_proba(features)[0]
                    risk_classes = ['low', 'medium', 'high']
                    risk_scores = {risk_classes[i]: float(prob) for i, prob in enumerate(probabilities)}
                    confidence = float(max(probabilities))
                except:
                    risk_scores = {risk_prediction: 0.8, 'low': 0.1, 'medium': 0.1}
                    confidence = 0.8
            else:
                risk_prediction, risk_scores, confidence = self._heuristic_risk_assessment(
                    temperature, humidity, rainfall, wind_speed, pressure, location
                )
            
            # Generate detailed risk analysis
            risk_factors = self._analyze_risk_factors(temperature, humidity, rainfall, wind_speed, pressure)
            recommendations = self._generate_recommendations(risk_prediction, risk_factors, crop)
            
            # Legacy compatibility
            pest_probability = risk_scores.get('high', 0.3) if 'pest' in text.lower() or humidity > 70 else 0.2
            advice = recommendations[0] if recommendations else "Monitor crops regularly"
            
            return {
                "success": True,
                "location": location,
                "crop": crop,
                "time_period": time_period,
                "overall_risk_level": risk_prediction,
                "risk_scores": risk_scores,
                "confidence": confidence,
                "risk_factors": risk_factors,
                "recommendations": recommendations,
                "weather_conditions": {
                    "temperature": temperature,
                    "humidity": humidity,
                    "rainfall": rainfall,
                    "wind_speed": wind_speed,
                    "pressure": pressure
                },
                # Legacy fields for backward compatibility
                "pest_probability": round(pest_probability, 3),
                "yield_risk": risk_prediction in ['medium', 'high'],
                "advice": advice,
                "message": f"Risk assessment for {crop} in {location}: {risk_prediction.upper()} risk level. {self._get_risk_summary(risk_prediction, risk_factors)}",
                "agent_used": "risk"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Risk assessment failed: {str(e)}",
                "agent_used": "risk"
            }

    def _get_location_risk_score(self, location):
        """Get risk score for location (0-1, higher = more risky)"""
        # High-risk areas for agriculture
        high_risk_locations = ["desert", "coastal", "flood-prone", "drought-prone"]
        medium_risk_locations = ["hills", "semi-arid", "subtropical"]
        
        location_lower = location.lower()
        
        if any(term in location_lower for term in high_risk_locations):
            return 0.8
        elif any(term in location_lower for term in medium_risk_locations):
            return 0.5
        else:
            return 0.3

    def _heuristic_risk_assessment(self, temp, humidity, rainfall, wind_speed, pressure, location):
        """Heuristic-based risk assessment when model is not available"""
        risk_score = 0.0
        
        # Temperature risk
        if temp > 35 or temp < 5:
            risk_score += 0.3
        elif temp > 30 or temp < 10:
            risk_score += 0.1
        
        # Humidity risk
        if humidity > 90 or humidity < 20:
            risk_score += 0.2
        
        # Rainfall risk
        if rainfall > 200 or rainfall < 20:
            risk_score += 0.25
        
        # Wind speed risk
        if wind_speed > 25:
            risk_score += 0.15
        
        # Pressure risk
        if pressure < 990 or pressure > 1030:
            risk_score += 0.1
        
        # Location risk
        risk_score += self._get_location_risk_score(location) * 0.2
        
        # Determine risk level
        if risk_score > 0.6:
            risk_level = "high"
        elif risk_score > 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Create risk scores
        risk_scores = {
            "high": min(1.0, risk_score),
            "medium": max(0.0, min(1.0, 1.0 - abs(risk_score - 0.5))),
            "low": max(0.0, 1.0 - risk_score)
        }
        
        confidence = 0.7
        
        return risk_level, risk_scores, confidence

    def _analyze_risk_factors(self, temp, humidity, rainfall, wind_speed, pressure):
        """Analyze specific risk factors"""
        factors = []
        
        if temp > 35:
            factors.append({"factor": "extreme_heat", "severity": "high", "description": "Extreme heat can cause crop stress and reduce yields"})
        elif temp < 5:
            factors.append({"factor": "frost_risk", "severity": "high", "description": "Frost risk can damage or kill crops"})
        
        if humidity > 85:
            factors.append({"factor": "high_humidity", "severity": "medium", "description": "High humidity increases disease and pest risk"})
        elif humidity < 30:
            factors.append({"factor": "low_humidity", "severity": "medium", "description": "Low humidity can stress plants and reduce growth"})
        
        if rainfall > 200:
            factors.append({"factor": "excessive_rainfall", "severity": "high", "description": "Excessive rainfall can cause flooding and root rot"})
        elif rainfall < 25:
            factors.append({"factor": "drought_risk", "severity": "high", "description": "Insufficient rainfall increases drought stress risk"})
        
        if wind_speed > 25:
            factors.append({"factor": "strong_winds", "severity": "medium", "description": "Strong winds can damage crops and increase water loss"})
        
        if pressure < 995:
            factors.append({"factor": "low_pressure", "severity": "low", "description": "Low pressure may indicate approaching storms"})
        
        return factors

    def _generate_recommendations(self, risk_level, risk_factors, crop):
        """Generate recommendations based on risk assessment"""
        recommendations = []
        
        if risk_level == "high":
            recommendations.append("Consider delaying planting or harvesting until conditions improve")
            recommendations.append("Implement protective measures such as mulching or shade covers")
            recommendations.append("Ensure adequate insurance coverage for crop losses")
        
        if risk_level == "medium":
            recommendations.append("Monitor weather conditions closely")
            recommendations.append("Prepare contingency measures for potential risks")
        
        # Specific recommendations based on risk factors
        factor_types = [f["factor"] for f in risk_factors]
        
        if "drought_risk" in factor_types:
            recommendations.append("Install irrigation systems or increase water storage")
            recommendations.append("Consider drought-resistant crop varieties")
        
        if "excessive_rainfall" in factor_types:
            recommendations.append("Ensure proper drainage in fields")
            recommendations.append("Consider raised bed cultivation")
        
        if "extreme_heat" in factor_types:
            recommendations.append("Provide shade or cooling for sensitive crops")
            recommendations.append("Adjust irrigation schedule for increased water needs")
        
        if "high_humidity" in factor_types:
            recommendations.append("Improve air circulation around crops")
            recommendations.append("Apply preventive fungicide treatments")
        
        if "strong_winds" in factor_types:
            recommendations.append("Install windbreaks or protective barriers")
            recommendations.append("Stake tall crops securely")
        
        if not recommendations:
            recommendations.append("Conditions appear favorable for normal agricultural activities")
            recommendations.append("Continue regular monitoring and maintenance")
        
        return recommendations

    def _get_risk_summary(self, risk_level, risk_factors):
        """Get a brief summary of the risk assessment"""
        if not risk_factors:
            return "No significant risk factors identified."
        
        high_severity_factors = [f for f in risk_factors if f["severity"] == "high"]
        
        if high_severity_factors:
            main_risk = high_severity_factors[0]["factor"].replace("_", " ").title()
            return f"Main concern: {main_risk}. Take immediate protective action."
        elif risk_factors:
            main_risk = risk_factors[0]["factor"].replace("_", " ").title()
            return f"Monitor: {main_risk}. Prepare contingency measures."
        else:
            return "Generally favorable conditions."

    def process_query(self, text: str, payload: dict) -> dict:
        """Process query using the predict method"""
        return self.predict(payload)

    def format_result_text(self, result, context):
        """Format result into readable text"""
        if not result.get("success"):
            return f"Unable to assess agricultural risks: {result.get('error', 'Unknown error')}"
        
        # Legacy format support
        if "pest_probability" in result:
            return f"Pest outbreak probability {result['pest_probability']*100:.1f}%. {result.get('advice', 'Monitor crops regularly')}"
        
        risk_level = result.get("overall_risk_level", "unknown")
        location = result.get("location", "your area")
        crop = result.get("crop", "crops")
        
        risk_factors = result.get("risk_factors", [])
        if risk_factors:
            main_factors = [f["factor"].replace("_", " ") for f in risk_factors[:2]]
            factors_text = f" Main concerns: {', '.join(main_factors)}."
        else:
            factors_text = " No major risk factors identified."
        
        return f"Risk assessment for {crop} in {location}: {risk_level.upper()} risk level.{factors_text}"
