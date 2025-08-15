from .base_agent import BaseAgent
import numpy as np
from typing import Dict, Any, Optional
import cv2
import onnxruntime as ort

class PestAgent(BaseAgent):
    """Agent for pest and disease prediction from images/video"""
    
    def __init__(self):
        super().__init__()
        self.model_path = "models/cloud/pest_model.onnx"
        self.session = None
        self._load_model()
    
    def _load_model(self):
        """Load the ONNX pest detection model"""
        try:
            self.session = ort.InferenceSession(self.model_path)
            self.logger.info("Pest detection model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load pest model: {e}")
    
    def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process pest/disease detection query
        
        Args:
            query: User query about pest/disease
            context: Additional context including image data
            
        Returns:
            Dict containing pest detection results
        """
        try:
            image_data = context.get('image_data')
            if not image_data:
                return {
                    "error": "No image data provided for pest detection",
                    "agent": "pest_agent"
                }
            
            # Preprocess image
            processed_image = self._preprocess_image(image_data)
            
            # Run inference
            predictions = self._predict(processed_image)
            
            # Post-process results
            results = self._postprocess_predictions(predictions)
            
            return {
                "agent": "pest_agent",
                "predictions": results,
                "confidence_scores": predictions.get("confidence", []),
                "detected_pests": results.get("pests", []),
                "treatment_recommendations": self._get_treatment_recommendations(results)
            }
            
        except Exception as e:
            self.logger.error(f"Error in pest detection: {e}")
            return {
                "error": f"Pest detection failed: {str(e)}",
                "agent": "pest_agent"
            }
    
    def _preprocess_image(self, image_data: bytes) -> np.ndarray:
        """Preprocess image for model input"""
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Resize to model input size (assuming 224x224)
        image = cv2.resize(image, (224, 224))
        
        # Normalize
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def _predict(self, image: np.ndarray) -> Dict[str, Any]:
        """Run model inference"""
        if not self.session:
            raise Exception("Model not loaded")
        
        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: image})
        
        return {
            "predictions": outputs[0],
            "confidence": outputs[0].max(axis=1)
        }
    
    def _postprocess_predictions(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        """Post-process model predictions"""
        # Mock pest classes - replace with actual model classes
        pest_classes = [
            "Aphids", "Spider Mites", "Whiteflies", "Thrips", 
            "Caterpillars", "Leaf Miners", "Scale Insects", "Healthy"
        ]
        
        pred_array = predictions["predictions"][0]
        top_indices = np.argsort(pred_array)[-3:][::-1]  # Top 3 predictions
        
        results = {
            "pests": [],
            "confidence_scores": []
        }
        
        for idx in top_indices:
            if pred_array[idx] > 0.1:  # Confidence threshold
                results["pests"].append({
                    "name": pest_classes[idx],
                    "confidence": float(pred_array[idx]),
                    "severity": self._assess_severity(pred_array[idx])
                })
        
        return results
    
    def _assess_severity(self, confidence: float) -> str:
        """Assess pest infestation severity"""
        if confidence > 0.8:
            return "High"
        elif confidence > 0.5:
            return "Medium"
        else:
            return "Low"
    
    def _get_treatment_recommendations(self, results: Dict[str, Any]) -> list:
        """Get treatment recommendations based on detected pests"""
        recommendations = []
        
        for pest in results.get("pests", []):
            pest_name = pest["name"]
            severity = pest["severity"]
            
            if pest_name == "Aphids":
                if severity == "High":
                    recommendations.append("Apply systemic insecticide immediately")
                else:
                    recommendations.append("Use neem oil spray or introduce ladybugs")
            
            elif pest_name == "Spider Mites":
                recommendations.append("Increase humidity and apply miticide")
            
            elif pest_name == "Whiteflies":
                recommendations.append("Use yellow sticky traps and insecticidal soap")
            
            # Add more pest-specific recommendations
            
        return recommendations if recommendations else ["No specific treatment needed - monitor regularly"]