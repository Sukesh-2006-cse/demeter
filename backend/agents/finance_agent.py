import os
import joblib
import numpy as np
from .base_agent import BaseAgent

class FinanceAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("finance", models_dir=models_dir)
        
        # Try to load finance model from multiple locations
        model_paths = [
            os.path.join("models", "finance_model.pkl"),
            os.path.join(models_dir or "", "finance_model.pkl"),
        ]
        
        self.model = None
        for path in model_paths:
            if os.path.exists(path):
                try:
                    self.model = joblib.load(path)
                    print(f"Loaded finance model from {path}")
                    break
                except Exception as e:
                    print(f"Failed to load finance model from {path}: {e}")
        
        if self.model is None:
            print("Warning: Could not load finance model. Using heuristic predictions.")
        
        # Government schemes database
        self.schemes = [
            {"name": "PM-KISAN", "min_acre": 0, "max_amount": 6000, "description": "Direct income support"},
            {"name": "PMFBY Insurance", "min_acre": 0.1, "max_amount": 50000, "description": "Crop insurance"},
            {"name": "Drip Subsidy", "min_acre": 0.5, "max_amount": 40000, "description": "Irrigation subsidy"},
            {"name": "Kisan Credit Card", "min_acre": 1.0, "max_amount": 300000, "description": "Agricultural credit"}
        ]

    def predict(self, payload: dict) -> dict:
        """Main prediction method for agricultural finance assessment"""
        context = payload.get("context", {})
        text = payload.get("text", "")
        
        try:
            # Extract financial parameters from context
            farmer_profile = self._extract_farmer_profile(context, text)
            
            if self.model:
                # Use ML model for prediction
                features = self._prepare_features(farmer_profile)
                eligibility_prediction = self.model.predict([features])[0]
                
                # Get probabilities if available
                try:
                    probabilities = self.model.predict_proba([features])[0]
                    eligibility_classes = self.model.classes_
                    eligibility_scores = {eligibility_classes[i]: float(prob) for i, prob in enumerate(probabilities)}
                    confidence = float(max(probabilities))
                except:
                    eligibility_scores = {eligibility_prediction: 0.7}
                    confidence = 0.7
            else:
                # Fallback heuristic prediction
                eligibility_prediction, eligibility_scores, confidence = self._heuristic_finance_assessment(farmer_profile)
            
            # Generate financial recommendations
            eligible_schemes = self._get_eligible_schemes(eligibility_prediction, farmer_profile)
            financial_tips = self._get_financial_tips(farmer_profile)
            
            return {
                "success": True,
                "farmer_profile": farmer_profile,
                "eligibility_status": eligibility_prediction,
                "eligibility_scores": eligibility_scores,
                "confidence": confidence,
                "eligible_schemes": [scheme["name"] for scheme in eligible_schemes],
                "detailed_schemes": eligible_schemes,
                "financial_tips": financial_tips,
                "financial_health_score": self._calculate_financial_health_score(farmer_profile),
                "message": f"Finance assessment: {eligibility_prediction.upper()}. {len(eligible_schemes)} schemes available.",
                "agent_used": "finance"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Finance assessment failed: {str(e)}",
                "agent_used": "finance"
            }

    def _extract_farmer_profile(self, context, text):
        """Extract farmer financial profile from context and text"""
        
        # Extract from context with defaults
        profile = {
            "annual_income": float(context.get("annual_income", context.get("income", 150000))),
            "land_size_acres": float(context.get("land_size", context.get("area", context.get("area_hectares", 2.0)))),
            "credit_score": int(context.get("credit_score", 650)),
            "region": context.get("region", context.get("location", "general"))
        }
        
        return profile

    def _prepare_features(self, profile):
        """Prepare features for ML model"""
        # Features: income, land_size, credit_score, crop_value, location_score
        location_score = 0.5  # Default location score
        
        features = [
            profile["annual_income"] / 100000,  # Normalize income
            profile["land_size_acres"],
            profile["credit_score"] / 850,  # Normalize credit score
            profile["annual_income"] * 0.3 / 100000,  # Estimated crop value
            location_score
        ]
        
        return features

    def _heuristic_finance_assessment(self, profile):
        """Heuristic-based finance assessment when model is not available"""
        
        eligibility_score = 0.0
        
        # Income assessment
        if profile["annual_income"] > 300000:
            eligibility_score += 0.4
        elif profile["annual_income"] > 150000:
            eligibility_score += 0.2
        elif profile["annual_income"] > 50000:
            eligibility_score += 0.1
        
        # Credit score assessment
        if profile["credit_score"] > 750:
            eligibility_score += 0.3
        elif profile["credit_score"] > 650:
            eligibility_score += 0.2
        elif profile["credit_score"] > 550:
            eligibility_score += 0.1
        
        # Land size assessment
        if profile["land_size_acres"] > 5:
            eligibility_score += 0.3
        elif profile["land_size_acres"] > 2:
            eligibility_score += 0.2
        elif profile["land_size_acres"] > 0.5:
            eligibility_score += 0.1
        
        # Determine eligibility level
        if eligibility_score > 0.7:
            eligibility = "eligible"
        elif eligibility_score > 0.4:
            eligibility = "partial_eligible"
        else:
            eligibility = "not_eligible"
        
        # Create eligibility scores
        eligibility_scores = {
            "eligible": min(1.0, eligibility_score),
            "partial_eligible": max(0.0, min(1.0, 1.0 - abs(eligibility_score - 0.5))),
            "not_eligible": max(0.0, 1.0 - eligibility_score)
        }
        
        confidence = 0.75
        
        return eligibility, eligibility_scores, confidence

    def _get_eligible_schemes(self, eligibility, profile):
        """Get list of eligible schemes based on profile"""
        
        eligible = []
        land_acres = profile["land_size_acres"]
        
        for scheme in self.schemes:
            if land_acres >= scheme["min_acre"]:
                # Add eligibility criteria based on assessment
                if eligibility == "not_eligible" and scheme["name"] in ["Kisan Credit Card"]:
                    continue  # Skip credit-based schemes for non-eligible farmers
                
                eligible.append({
                    "name": scheme["name"],
                    "max_amount": scheme["max_amount"],
                    "description": scheme["description"],
                    "eligibility_status": eligibility
                })
        
        return eligible

    def _get_financial_tips(self, profile):
        """Get financial tips based on farmer profile"""
        
        tips = []
        
        if profile["credit_score"] < 650:
            tips.append("Focus on improving credit score by paying loans on time")
        
        if profile["land_size_acres"] < 2:
            tips.append("Consider crop intensification to maximize returns from limited land")
        
        if profile["annual_income"] < 200000:
            tips.append("Explore value-added agriculture and direct marketing")
        
        tips.append(f"Farmers in {profile['region']} often benefit from cooperative farming")
        tips.append("Consider diversifying income with allied activities like poultry or dairy")
        
        return tips

    def _calculate_financial_health_score(self, profile):
        """Calculate overall financial health score (0-100)"""
        
        score = 0
        
        # Income component (40%)
        income_score = min(40, (profile["annual_income"] / 500000) * 40)
        score += income_score
        
        # Credit score component (35%)
        credit_score_component = (profile["credit_score"] / 850) * 35
        score += credit_score_component
        
        # Land asset component (25%)
        land_score = min(25, profile["land_size_acres"] * 5)
        score += land_score
        
        return min(100, int(score))

    def process_query(self, text: str, payload: dict) -> dict:
        """Process query using the predict method"""
        return self.predict(payload)

    def format_result_text(self, result, context):
        """Format result into readable text"""
        if not result.get("success"):
            return f"Unable to assess finance options: {result.get('error', 'Unknown error')}"
        
        schemes = result.get("eligible_schemes", [])
        tips = result.get("financial_tips", [])
        
        if schemes:
            schemes_text = f"Eligible schemes: {', '.join(schemes[:3])}"
        else:
            schemes_text = "Limited financing options available"
        
        main_tip = tips[0] if tips else "Consider improving financial documentation"
        
        return f"{schemes_text}. Tip: {main_tip}"
