"""
Post-processing utilities for model outputs
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ModelOutputProcessor:
    """Post-processing utilities for model outputs"""
    
    def __init__(self):
        self.confidence_threshold = 0.7
    
    def process_crop_recommendations(self, predictions: np.ndarray, 
                                   crop_classes: List[str], 
                                   top_k: int = 3) -> Dict[str, Any]:
        """
        Process crop recommendation model output
        
        Args:
            predictions: Model prediction probabilities
            crop_classes: List of crop class names
            top_k: Number of top recommendations to return
            
        Returns:
            Processed recommendations with confidence scores
        """
        try:
            # Get top-k predictions
            top_indices = np.argsort(predictions)[-top_k:][::-1]
            
            recommendations = []
            for idx in top_indices:
                confidence = float(predictions[idx])
                if confidence >= self.confidence_threshold:
                    recommendations.append({
                        'crop': crop_classes[idx],
                        'confidence': confidence,
                        'suitability': self._assess_suitability(confidence),
                        'reasons': self._get_crop_reasons(crop_classes[idx], confidence)
                    })
            
            return {
                'recommendations': recommendations,
                'total_confidence': float(np.sum([r['confidence'] for r in recommendations])),
                'status': 'success' if recommendations else 'low_confidence'
            }
            
        except Exception as e:
            logger.error(f"Error processing crop recommendations: {e}")
            return {'error': str(e), 'status': 'error'}
    
    def process_market_predictions(self, predictions: np.ndarray, 
                                 historical_prices: List[float],
                                 time_horizon: int = 30) -> Dict[str, Any]:
        """
        Process market price prediction output
        
        Args:
            predictions: Predicted prices
            historical_prices: Historical price data
            time_horizon: Prediction time horizon in days
            
        Returns:
            Processed market analysis
        """
        try:
            current_price = historical_prices[-1] if historical_prices else 0
            predicted_price = float(predictions[-1]) if len(predictions) > 0 else current_price
            
            # Calculate price change
            price_change = predicted_price - current_price
            price_change_percent = (price_change / current_price) * 100 if current_price > 0 else 0
            
            # Assess trend
            trend = self._assess_price_trend(predictions, historical_prices)
            
            # Calculate volatility
            volatility = self._calculate_volatility(predictions)
            
            # Generate trading signals
            signals = self._generate_trading_signals(predictions, historical_prices)
            
            return {
                'current_price': current_price,
                'predicted_price': predicted_price,
                'price_change': price_change,
                'price_change_percent': price_change_percent,
                'trend': trend,
                'volatility': volatility,
                'signals': signals,
                'confidence': self._calculate_prediction_confidence(predictions),
                'time_horizon_days': time_horizon,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error processing market predictions: {e}")
            return {'error': str(e), 'status': 'error'}
    
    def process_yield_predictions(self, predictions: np.ndarray,
                                crop_type: str,
                                area_hectares: float) -> Dict[str, Any]:
        """
        Process crop yield prediction output
        
        Args:
            predictions: Predicted yield values
            crop_type: Type of crop
            area_hectares: Cultivation area in hectares
            
        Returns:
            Processed yield analysis
        """
        try:
            predicted_yield_per_hectare = float(predictions[0]) if len(predictions) > 0 else 0
            total_predicted_yield = predicted_yield_per_hectare * area_hectares
            
            # Get benchmark yields for comparison
            benchmark_yield = self._get_benchmark_yield(crop_type)
            
            # Calculate performance metrics
            yield_performance = (predicted_yield_per_hectare / benchmark_yield) * 100 if benchmark_yield > 0 else 0
            
            # Assess yield category
            yield_category = self._categorize_yield(yield_performance)
            
            # Generate recommendations
            recommendations = self._generate_yield_recommendations(yield_performance, crop_type)
            
            return {
                'predicted_yield_per_hectare': predicted_yield_per_hectare,
                'total_predicted_yield': total_predicted_yield,
                'area_hectares': area_hectares,
                'benchmark_yield': benchmark_yield,
                'yield_performance_percent': yield_performance,
                'yield_category': yield_category,
                'recommendations': recommendations,
                'crop_type': crop_type,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error processing yield predictions: {e}")
            return {'error': str(e), 'status': 'error'}
    
    def process_risk_assessment(self, risk_scores: np.ndarray,
                              risk_factors: List[str]) -> Dict[str, Any]:
        """
        Process risk assessment model output
        
        Args:
            risk_scores: Risk probability scores
            risk_factors: List of risk factor names
            
        Returns:
            Processed risk analysis
        """
        try:
            risk_analysis = []
            overall_risk = 0
            
            for i, (score, factor) in enumerate(zip(risk_scores, risk_factors)):
                risk_level = self._categorize_risk(float(score))
                risk_analysis.append({
                    'factor': factor,
                    'probability': float(score),
                    'risk_level': risk_level,
                    'mitigation_strategies': self._get_mitigation_strategies(factor, risk_level)
                })
                overall_risk += score
            
            overall_risk = overall_risk / len(risk_scores) if risk_scores.size > 0 else 0
            overall_risk_level = self._categorize_risk(overall_risk)
            
            # Priority risks (top 3)
            priority_risks = sorted(risk_analysis, key=lambda x: x['probability'], reverse=True)[:3]
            
            return {
                'overall_risk_score': float(overall_risk),
                'overall_risk_level': overall_risk_level,
                'risk_factors': risk_analysis,
                'priority_risks': priority_risks,
                'total_factors_assessed': len(risk_factors),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error processing risk assessment: {e}")
            return {'error': str(e), 'status': 'error'}
    
    def _assess_suitability(self, confidence: float) -> str:
        """Assess crop suitability based on confidence"""
        if confidence >= 0.8:
            return "Highly Suitable"
        elif confidence >= 0.6:
            return "Suitable"
        elif confidence >= 0.4:
            return "Moderately Suitable"
        else:
            return "Not Suitable"
    
    def _get_crop_reasons(self, crop: str, confidence: float) -> List[str]:
        """Get reasons for crop recommendation"""
        reasons = []
        
        if confidence >= 0.8:
            reasons.append(f"Excellent soil and climate conditions for {crop}")
            reasons.append("High expected yield potential")
        elif confidence >= 0.6:
            reasons.append(f"Good growing conditions for {crop}")
            reasons.append("Moderate to high yield expected")
        else:
            reasons.append(f"Some challenges expected for {crop}")
            reasons.append("Consider soil amendments or climate protection")
        
        return reasons
    
    def _assess_price_trend(self, predictions: np.ndarray, historical: List[float]) -> str:
        """Assess price trend direction"""
        if len(predictions) < 2:
            return "Insufficient data"
        
        recent_trend = np.mean(predictions[-3:]) - np.mean(predictions[:3])
        
        if recent_trend > 0.05:
            return "Upward"
        elif recent_trend < -0.05:
            return "Downward"
        else:
            return "Stable"
    
    def _calculate_volatility(self, predictions: np.ndarray) -> float:
        """Calculate price volatility"""
        if len(predictions) < 2:
            return 0.0
        return float(np.std(predictions))
    
    def _generate_trading_signals(self, predictions: np.ndarray, historical: List[float]) -> List[str]:
        """Generate trading signals"""
        signals = []
        
        if len(predictions) == 0:
            return ["Insufficient data for signals"]
        
        current_price = historical[-1] if historical else predictions[0]
        future_price = predictions[-1]
        
        price_change_percent = ((future_price - current_price) / current_price) * 100
        
        if price_change_percent > 10:
            signals.append("Strong Buy Signal - Significant price increase expected")
        elif price_change_percent > 5:
            signals.append("Buy Signal - Price increase expected")
        elif price_change_percent < -10:
            signals.append("Strong Sell Signal - Significant price decrease expected")
        elif price_change_percent < -5:
            signals.append("Sell Signal - Price decrease expected")
        else:
            signals.append("Hold Signal - Price expected to remain stable")
        
        return signals
    
    def _calculate_prediction_confidence(self, predictions: np.ndarray) -> float:
        """Calculate confidence in predictions"""
        if len(predictions) < 2:
            return 0.5
        
        # Lower volatility = higher confidence
        volatility = np.std(predictions)
        mean_price = np.mean(predictions)
        
        if mean_price == 0:
            return 0.5
        
        coefficient_of_variation = volatility / mean_price
        confidence = max(0.1, min(0.9, 1 - coefficient_of_variation))
        
        return float(confidence)
    
    def _get_benchmark_yield(self, crop_type: str) -> float:
        """Get benchmark yield for crop type"""
        # Mock benchmark yields (tons per hectare)
        benchmarks = {
            'wheat': 3.5,
            'rice': 4.5,
            'corn': 6.0,
            'soybeans': 2.8,
            'cotton': 1.2,
            'tomatoes': 45.0,
            'potatoes': 25.0
        }
        
        return benchmarks.get(crop_type.lower(), 3.0)
    
    def _categorize_yield(self, performance_percent: float) -> str:
        """Categorize yield performance"""
        if performance_percent >= 120:
            return "Excellent"
        elif performance_percent >= 100:
            return "Good"
        elif performance_percent >= 80:
            return "Average"
        elif performance_percent >= 60:
            return "Below Average"
        else:
            return "Poor"
    
    def _generate_yield_recommendations(self, performance: float, crop_type: str) -> List[str]:
        """Generate yield improvement recommendations"""
        recommendations = []
        
        if performance < 80:
            recommendations.extend([
                "Consider soil testing and nutrient management",
                "Evaluate irrigation efficiency",
                "Review pest and disease management practices"
            ])
        
        if performance < 100:
            recommendations.extend([
                "Optimize fertilizer application timing",
                "Consider improved seed varieties",
                "Monitor weather conditions closely"
            ])
        
        # Crop-specific recommendations
        if crop_type.lower() == 'wheat':
            recommendations.append("Consider nitrogen application at tillering stage")
        elif crop_type.lower() == 'rice':
            recommendations.append("Maintain proper water levels during grain filling")
        
        return recommendations if recommendations else ["Current practices appear optimal"]
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk level"""
        if risk_score >= 0.8:
            return "Very High"
        elif risk_score >= 0.6:
            return "High"
        elif risk_score >= 0.4:
            return "Medium"
        elif risk_score >= 0.2:
            return "Low"
        else:
            return "Very Low"
    
    def _get_mitigation_strategies(self, risk_factor: str, risk_level: str) -> List[str]:
        """Get mitigation strategies for specific risks"""
        strategies = {
            'drought': [
                "Install drip irrigation systems",
                "Use drought-resistant crop varieties",
                "Implement water conservation practices",
                "Consider crop insurance"
            ],
            'flood': [
                "Improve drainage systems",
                "Plant on raised beds",
                "Use flood-tolerant varieties",
                "Monitor weather forecasts closely"
            ],
            'pest': [
                "Implement integrated pest management",
                "Use biological control agents",
                "Regular field monitoring",
                "Rotate crops to break pest cycles"
            ],
            'disease': [
                "Use disease-resistant varieties",
                "Improve air circulation",
                "Apply preventive fungicides",
                "Remove infected plant material"
            ],
            'market': [
                "Diversify crop portfolio",
                "Use forward contracts",
                "Monitor market trends",
                "Consider value-added processing"
            ]
        }
        
        factor_key = risk_factor.lower()
        base_strategies = strategies.get(factor_key, ["Consult agricultural extension services"])
        
        if risk_level in ["Very High", "High"]:
            return base_strategies
        else:
            return base_strategies[:2]  # Return fewer strategies for lower risk