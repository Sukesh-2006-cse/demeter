import os
import joblib
import numpy as np
import base64
from .base_agent import BaseAgent

class PestAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("pest", models_dir=models_dir)
        
        # Try to load pest detection model from multiple locations
        model_paths = [
            os.path.join("models", "pest_model.pkl"),
            os.path.join(models_dir or "", "pest_model.pkl"),
        ]
        
        self.model = None
        for path in model_paths:
            if os.path.exists(path):
                try:
                    self.model = joblib.load(path)
                    print(f"Loaded pest model from {path}")
                    break
                except Exception as e:
                    print(f"Failed to load pest model from {path}: {e}")
        
        if self.model is None:
            print("Warning: Could not load pest model. Using heuristic predictions.")

    def predict(self, payload: dict) -> dict:
        """Main prediction method for pest detection"""
        context = payload.get("context", {})
        text = payload.get("text", "")
        
        try:
            # Extract image data and other parameters
            image_data = context.get("image_data", context.get("image"))
            crop_type = context.get("crop_type", "unknown")
            symptoms = context.get("symptoms", [])
            
            if not image_data:
                return {
                    "success": False,
                    "error": "No image data provided for pest detection",
                    "agent_used": "pest"
                }
            
            # Process image and extract features
            image_features = self._extract_image_features(image_data)
            
            if self.model:
                # Use ML model for prediction
                features = np.array([image_features])
                pest_prediction = self.model.predict(features)[0]
                
                # Get probabilities if available
                try:
                    probabilities = self.model.predict_proba(features)[0]
                    pest_classes = self.model.classes_
                    pest_scores = {pest_classes[i]: float(prob) for i, prob in enumerate(probabilities)}
                    confidence = float(max(probabilities))
                    
                    # Get top 3 predictions
                    top_indices = probabilities.argsort()[-3:][::-1]
                    top_pests = [pest_classes[i] for i in top_indices]
                    top_confidences = [float(probabilities[i]) for i in top_indices]
                except:
                    pest_scores = {pest_prediction: 0.7}
                    confidence = 0.7
                    top_pests = [pest_prediction]
                    top_confidences = [0.7]
            else:
                # Fallback heuristic prediction
                pest_prediction, pest_scores, confidence, top_pests, top_confidences = self._heuristic_pest_detection(
                    crop_type, symptoms, image_features
                )
            
            # Generate treatment recommendations
            treatment_recommendations = self._generate_treatment_recommendations(pest_prediction, crop_type)
            prevention_tips = self._generate_prevention_tips(pest_prediction, crop_type)
            
            return {
                "success": True,
                "detected_pest": pest_prediction,
                "pest_type": pest_prediction,
                "confidence": confidence,
                "crop_type": crop_type,
                "pest_scores": pest_scores,
                "top_predictions": [
                    {"pest": pest, "confidence": conf} 
                    for pest, conf in zip(top_pests, top_confidences)
                ],
                "treatment_recommendations": treatment_recommendations,
                "prevention_tips": prevention_tips,
                "severity_assessment": self._assess_severity(confidence, pest_prediction),
                "immediate_actions": self._get_immediate_actions(pest_prediction),
                "message": f"Detected {pest_prediction} with {confidence:.1%} confidence. {self._get_pest_summary(pest_prediction, confidence)}",
                "agent_used": "pest"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Pest detection failed: {str(e)}",
                "agent_used": "pest"
            }

    def _extract_image_features(self, image_data):
        """Extract features from image data (simplified for demo)"""
        try:
            # In a real implementation, this would use computer vision
            # to extract meaningful features from the image
            # For now, we'll create dummy features based on image data
            
            if isinstance(image_data, str):
                # If it's base64 encoded, decode and get length
                try:
                    decoded = base64.b64decode(image_data)
                    image_size = len(decoded)
                except:
                    image_size = len(image_data)
            else:
                image_size = len(str(image_data))
            
            # Create dummy features (in real implementation, use CNN features)
            np.random.seed(image_size % 1000)  # Pseudo-random based on image
            features = np.random.rand(100).tolist()  # 100 features
            
            return features
            
        except Exception as e:
            print(f"Error extracting image features: {e}")
            # Return default features
            return np.random.rand(100).tolist()

    def _heuristic_pest_detection(self, crop_type, symptoms, image_features):
        """Heuristic-based pest detection when model is not available"""
        
        # Common pests by crop type
        crop_pests = {
            "wheat": ["armyworm", "aphid", "stem_borer"],
            "rice": ["brown_planthopper", "stem_borer", "leaf_miner"],
            "corn": ["armyworm", "bollworm", "cutworm"],
            "cotton": ["bollworm", "whitefly", "aphid"],
            "tomato": ["fruit_borer", "whitefly", "thrips"],
            "potato": ["cutworm", "aphid", "leaf_miner"]
        }
        
        # Default pest list
        default_pests = ["armyworm", "aphid", "bollworm", "cutworm", "thrips", "whitefly"]
        
        # Get possible pests for this crop
        possible_pests = crop_pests.get(crop_type.lower(), default_pests)
        
        # Use image features to determine most likely pest
        feature_sum = sum(image_features[:10]) if len(image_features) >= 10 else 5.0
        pest_index = int(feature_sum) % len(possible_pests)
        predicted_pest = possible_pests[pest_index]
        
        # Create confidence based on symptoms match
        base_confidence = 0.6
        if symptoms:
            # Increase confidence if symptoms are provided
            symptom_keywords = ["spots", "holes", "yellowing", "wilting", "damage"]
            if any(keyword in " ".join(symptoms).lower() for keyword in symptom_keywords):
                base_confidence += 0.1
        
        # Create pest scores
        pest_scores = {}
        for i, pest in enumerate(possible_pests[:3]):
            if pest == predicted_pest:
                pest_scores[pest] = base_confidence
            else:
                pest_scores[pest] = max(0.1, base_confidence - 0.2 * (i + 1))
        
        top_pests = list(pest_scores.keys())
        top_confidences = list(pest_scores.values())
        
        return predicted_pest, pest_scores, base_confidence, top_pests, top_confidences

    def _generate_treatment_recommendations(self, pest, crop_type):
        """Generate treatment recommendations for detected pest"""
        
        treatments = {
            "armyworm": [
                "Apply Bacillus thuringiensis (Bt) spray",
                "Use pheromone traps to monitor populations",
                "Apply neem-based insecticides",
                "Consider releasing natural predators like Trichogramma"
            ],
            "aphid": [
                "Spray with insecticidal soap solution",
                "Use neem oil spray",
                "Introduce ladybugs as biological control",
                "Remove affected plant parts"
            ],
            "bollworm": [
                "Apply targeted insecticides during larval stage",
                "Use pheromone traps for monitoring",
                "Plant trap crops around main field",
                "Apply Bt-based biological pesticides"
            ],
            "whitefly": [
                "Use yellow sticky traps",
                "Apply horticultural oil sprays",
                "Introduce Encarsia parasitoids",
                "Maintain proper plant spacing for air circulation"
            ],
            "thrips": [
                "Use blue sticky traps",
                "Apply predatory mites as biological control",
                "Spray with spinosad-based insecticides",
                "Remove weeds that harbor thrips"
            ]
        }
        
        return treatments.get(pest, [
            "Consult local agricultural extension office",
            "Take sample to agricultural laboratory for identification",
            "Apply general-purpose organic insecticide",
            "Monitor pest population regularly"
        ])

    def _generate_prevention_tips(self, pest, crop_type):
        """Generate prevention tips for detected pest"""
        
        prevention = {
            "armyworm": [
                "Practice crop rotation",
                "Remove crop residues after harvest",
                "Monitor fields regularly during peak season",
                "Maintain beneficial insect habitats"
            ],
            "aphid": [
                "Avoid over-fertilization with nitrogen",
                "Plant companion crops like marigolds",
                "Maintain proper field sanitation",
                "Use reflective mulches"
            ],
            "bollworm": [
                "Plant early to avoid peak infestation period",
                "Use resistant crop varieties",
                "Maintain proper plant spacing",
                "Remove volunteer plants"
            ],
            "whitefly": [
                "Use virus-free planting material",
                "Control weeds in and around fields",
                "Avoid overlapping cropping seasons",
                "Use reflective mulches"
            ],
            "thrips": [
                "Remove weeds and alternate hosts",
                "Use proper irrigation management",
                "Plant windbreaks to reduce thrips movement",
                "Avoid excessive nitrogen fertilization"
            ]
        }
        
        return prevention.get(pest, [
            "Practice integrated pest management",
            "Monitor crops regularly",
            "Maintain field hygiene",
            "Use pest-resistant varieties when available"
        ])

    def _assess_severity(self, confidence, pest):
        """Assess the severity of the pest infestation"""
        if confidence > 0.8:
            return "High - Immediate action required"
        elif confidence > 0.6:
            return "Medium - Monitor closely and prepare treatment"
        else:
            return "Low - Continue monitoring"

    def _get_immediate_actions(self, pest):
        """Get immediate actions for detected pest"""
        immediate_actions = {
            "armyworm": "Check for egg masses and larvae, apply Bt spray if larvae present",
            "aphid": "Spray with water to dislodge, apply insecticidal soap if population is high",
            "bollworm": "Check for bore holes and larvae, apply targeted treatment",
            "whitefly": "Install yellow sticky traps, check undersides of leaves",
            "thrips": "Install blue sticky traps, check for silvering damage on leaves"
        }
        
        return immediate_actions.get(pest, "Take clear photos and consult agricultural expert")

    def _get_pest_summary(self, pest, confidence):
        """Get a brief summary of the pest detection"""
        if confidence > 0.8:
            return f"High confidence detection. Take immediate action against {pest}."
        elif confidence > 0.6:
            return f"Moderate confidence. Monitor closely and prepare treatment for {pest}."
        else:
            return f"Low confidence detection. Continue monitoring for {pest} symptoms."

    def process_query(self, text: str, payload: dict) -> dict:
        """Process query using the predict method"""
        return self.predict(payload)

    def format_result_text(self, result, context):
        """Format result into readable text"""
        if not result.get("success"):
            return f"Unable to detect pest: {result.get('error', 'Unknown error')}"
        
        pest = result.get("detected_pest", "unknown pest")
        confidence = result.get("confidence", 0)
        severity = result.get("severity_assessment", "unknown")
        
        return f"Detected: {pest.replace('_', ' ').title()} (Confidence: {confidence:.1%}, Severity: {severity})"