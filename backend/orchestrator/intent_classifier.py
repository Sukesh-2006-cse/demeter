"""
Advanced intent classifier using machine learning to determine which agent should handle the query
"""
import re
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import json
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)

class AdvancedIntentClassifier:
    """Advanced ML-based intent classifier with NLP capabilities"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.pipeline = None
        self.intent_examples = self._load_training_data()
        self.parameter_extractors = self._initialize_extractors()
        self._train_model()
    
    def _load_training_data(self) -> Dict[str, List[str]]:
        """Load comprehensive training data for intent classification"""
        return {
            'crop_recommendation': [
                # Direct crop recommendation queries
                "What crop should I plant?",
                "Which crop is best for my soil?",
                "Recommend a crop for sandy soil",
                "What to grow in acidic soil?",
                "Best crop for high humidity area",
                "Crop recommendation for pH 6.5",
                "What should I plant this season?",
                "Which crop gives good yield in my climate?",
                "Suggest crops for nitrogen rich soil",
                "What crop is suitable for 25°C temperature?",
                
                # Soil-based queries
                "My soil has high nitrogen, what to plant?",
                "Low phosphorus soil crop suggestions",
                "Potassium deficient soil recommendations",
                "Clay soil best crops",
                "Sandy loam soil crop options",
                "Alkaline soil suitable crops",
                "Waterlogged soil crop choices",
                "Drought resistant crop suggestions",
                
                # Climate-based queries
                "Crops for tropical climate",
                "Cold weather crop recommendations",
                "Monsoon season planting advice",
                "Summer crop suggestions",
                "Winter farming options",
                "High rainfall area crops",
                "Low water requirement crops",
                "Heat tolerant crop varieties",
                
                # Specific condition queries
                "Crops for small farm",
                "High profit margin crops",
                "Quick growing crop options",
                "Organic farming crop suggestions",
                "Intercropping recommendations",
                "Crop rotation suggestions",
                "First time farmer crop advice",
                "Sustainable farming crops"
            ],
            
            'market_yield': [
                # Price prediction queries
                "What will be the price of wheat next month?",
                "Predict rice prices for this season",
                "Market forecast for corn",
                "Expected price trends for soybeans",
                "Will tomato prices increase?",
                "Price analysis for cotton",
                "Market outlook for sugarcane",
                "Commodity price predictions",
                
                # Yield prediction queries
                "How much yield can I expect?",
                "Predict my crop yield",
                "Expected harvest from 5 acres",
                "Yield forecast for wheat",
                "Production estimate for rice",
                "Harvest prediction for corn",
                "Expected output per hectare",
                "Crop productivity analysis",
                
                # Market analysis queries
                "Market demand for vegetables",
                "Supply chain analysis",
                "Best time to sell crops",
                "Market trends for fruits",
                "Export opportunities for grains",
                "Local market prices",
                "Wholesale vs retail pricing",
                "Seasonal price variations",
                
                # Economic queries
                "Profit margin analysis",
                "Cost-benefit of growing wheat",
                "Return on investment for farming",
                "Break-even analysis for crops",
                "Financial planning for harvest",
                "Revenue projections",
                "Market value assessment",
                "Economic viability study"
            ],
            
            'risk_assessment': [
                # Weather risk queries
                "What are the weather risks for my crop?",
                "Drought risk assessment",
                "Flood probability this season",
                "Climate change impact on farming",
                "Weather forecast for farming",
                "Risk of extreme temperatures",
                "Monsoon delay effects",
                "Heatwave impact on crops",
                
                # Environmental risk queries
                "Soil erosion risk factors",
                "Water scarcity assessment",
                "Pollution impact on crops",
                "Air quality effects on farming",
                "Groundwater depletion risks",
                "Salinity risk in soil",
                "Contamination assessment",
                "Environmental hazards",
                
                # Agricultural risk queries
                "Crop failure probability",
                "Pest outbreak risk",
                "Disease spread likelihood",
                "Market volatility risks",
                "Supply chain disruptions",
                "Input cost fluctuations",
                "Labor shortage risks",
                "Technology adoption risks",
                
                # Insurance and mitigation
                "Crop insurance recommendations",
                "Risk mitigation strategies",
                "Disaster preparedness for farms",
                "Emergency response planning",
                "Risk management techniques",
                "Preventive measures for crops",
                "Safety protocols for farming",
                "Contingency planning advice"
            ],
            
            'pest_detection': [
                # Direct pest identification
                "What pest is this?",
                "Identify this bug on my plant",
                "What's eating my crops?",
                "Pest identification help",
                "Bug recognition service",
                "Insect classification",
                "Parasite detection",
                "Harmful pest identification",
                
                # Disease identification
                "What disease does my plant have?",
                "Identify plant disease",
                "Crop disease diagnosis",
                "Fungal infection identification",
                "Bacterial disease detection",
                "Viral disease symptoms",
                "Plant pathology help",
                "Disease classification service",
                
                # Damage assessment
                "Assess crop damage",
                "Evaluate pest damage",
                "Disease severity analysis",
                "Infestation level assessment",
                "Crop health evaluation",
                "Plant condition analysis",
                "Damage extent estimation",
                "Health status check",
                
                # Treatment queries
                "How to treat this pest?",
                "Pesticide recommendations",
                "Organic pest control methods",
                "Disease treatment options",
                "Integrated pest management",
                "Biological control agents",
                "Chemical treatment advice",
                "Prevention strategies"
            ],
            
            'finance_agent': [
                # Financial planning
                "Farm loan requirements",
                "Agricultural credit options",
                "Subsidy information",
                "Government schemes for farmers",
                "Investment planning for agriculture",
                "Financial assistance programs",
                "Crop insurance details",
                "Banking services for farmers",
                
                # Cost analysis
                "Farming cost estimation",
                "Input cost calculation",
                "Operational expense planning",
                "Budget preparation for crops",
                "Cost optimization strategies",
                "Expense tracking methods",
                "Financial record keeping",
                "Accounting for agriculture",
                
                # Revenue optimization
                "Income maximization strategies",
                "Value addition opportunities",
                "Direct marketing options",
                "Cooperative farming benefits",
                "Contract farming details",
                "Export market access",
                "Processing unit setup",
                "Agribusiness opportunities"
            ]
        }
    
    def _initialize_extractors(self) -> Dict[str, Any]:
        """Initialize parameter extraction patterns and methods"""
        return {
            'numbers': re.compile(r'\b\d+\.?\d*\b'),
            'crops': [
                'wheat', 'rice', 'corn', 'maize', 'barley', 'oats', 'rye', 'millet',
                'soybean', 'soya', 'chickpea', 'lentil', 'pea', 'bean', 'groundnut',
                'cotton', 'jute', 'hemp', 'flax', 'sugarcane', 'sugar beet',
                'potato', 'sweet potato', 'cassava', 'yam', 'onion', 'garlic',
                'tomato', 'pepper', 'chili', 'eggplant', 'cucumber', 'pumpkin',
                'carrot', 'radish', 'turnip', 'cabbage', 'cauliflower', 'broccoli',
                'lettuce', 'spinach', 'kale', 'celery', 'parsley', 'coriander',
                'apple', 'orange', 'banana', 'grape', 'mango', 'papaya', 'guava',
                'coconut', 'date', 'fig', 'pomegranate', 'watermelon', 'melon',
                'grapes','jackfruit','sappota','lemon','custard apple'
            ],
            'soil_nutrients': {
                'nitrogen': ['nitrogen', 'n', 'nitrate', 'ammonia'],
                'phosphorus': ['phosphorus', 'p', 'phosphate'],
                'potassium': ['potassium', 'k', 'potash']
            },
            'weather_terms': [
                'temperature', 'humidity', 'rainfall', 'precipitation', 'wind',
                'pressure', 'drought', 'flood', 'storm', 'cyclone', 'hail'
            ],
            'time_expressions': {
                'day': ['day', 'daily', 'today', 'tomorrow'],
                'week': ['week', 'weekly', 'next week', 'this week'],
                'month': ['month', 'monthly', 'next month', 'this month'],
                'season': ['season', 'seasonal', 'spring', 'summer', 'monsoon', 'winter'],
                'year': ['year', 'yearly', 'annual', 'next year', 'this year']
            },
            'locations': re.compile(r'\b(?:in|at|near|around)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'),
            'measurements': {
                'area': ['acre', 'hectare', 'sq ft', 'square feet', 'sq m', 'square meter'],
                'weight': ['kg', 'kilogram', 'ton', 'tonne', 'quintal', 'pound', 'lb'],
                'volume': ['liter', 'litre', 'gallon', 'ml', 'milliliter'],
                'distance': ['meter', 'metre', 'km', 'kilometer', 'feet', 'ft', 'inch']
            }
        }
    
    def _train_model(self):
        """Train the intent classification model"""
        # Prepare training data
        texts = []
        labels = []
        
        for intent, examples in self.intent_examples.items():
            texts.extend(examples)
            labels.extend([intent] * len(examples))
        
        # Create pipeline with TF-IDF and Naive Bayes
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 3),
                max_features=5000,
                stop_words='english',
                lowercase=True,
                strip_accents='ascii'
            )),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        # Train the model
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                texts, labels, test_size=0.2, random_state=42, stratify=labels
            )
            
            self.pipeline.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.pipeline.predict(X_test)
            logger.info("Intent Classification Model Performance:")
            logger.info(classification_report(y_test, y_pred))
            
        except Exception as e:
            logger.error(f"Error training intent classifier: {e}")
            # Fallback to simple keyword matching
            self.pipeline = None
    
    def classify_intent(self, query: str, context: Dict[str, Any] = None) -> Tuple[str, float]:
        """
        Classify the intent of a user query using ML model
        
        Args:
            query: User query string
            context: Additional context (e.g., image data, location, user history)
            
        Returns:
            Tuple of (intent, confidence_score)
        """
        # Handle empty or very short queries
        if not query or len(query.strip()) < 3:
            return 'general', 0.3
        
        # Strong contextual indicators
        if context:
            # Image data strongly indicates pest detection
            if context.get('image_data') or context.get('image_path'):
                return 'pest_detection', 0.95
            
            # Location + weather data indicates risk assessment
            if context.get('weather_data') and context.get('location'):
                return 'risk_assessment', 0.85
            
            # Financial keywords in context
            if context.get('financial_context'):
                return 'finance_agent', 0.8
        
        # Use ML model if available
        if self.pipeline:
            try:
                # Get prediction probabilities
                probabilities = self.pipeline.predict_proba([query])[0]
                classes = self.pipeline.classes_
                
                # Get the best prediction
                best_idx = np.argmax(probabilities)
                best_intent = classes[best_idx]
                confidence = probabilities[best_idx]
                
                # Apply contextual boosting
                confidence = self._apply_contextual_boosting(
                    query, best_intent, confidence, context
                )
                
                return best_intent, float(confidence)
                
            except Exception as e:
                logger.error(f"Error in ML classification: {e}")
        
        # Fallback to enhanced keyword matching
        return self._fallback_classification(query, context)
    
    def _apply_contextual_boosting(self, query: str, intent: str, confidence: float, 
                                 context: Dict[str, Any] = None) -> float:
        """Apply contextual boosting to confidence scores"""
        boost = 0.0
        query_lower = query.lower()
        
        # Boost based on specific keywords
        intent_boosters = {
            'crop_recommendation': ['recommend', 'suggest', 'best', 'suitable', 'plant', 'grow'],
            'market_yield': ['price', 'market', 'yield', 'forecast', 'predict', 'profit'],
            'risk_assessment': ['risk', 'danger', 'threat', 'weather', 'climate', 'drought'],
            'pest_detection': ['pest', 'bug', 'disease', 'identify', 'what is this'],
            'finance_agent': ['loan', 'credit', 'subsidy', 'cost', 'budget', 'money']
        }
        
        if intent in intent_boosters:
            matching_keywords = sum(1 for keyword in intent_boosters[intent] 
                                  if keyword in query_lower)
            boost += matching_keywords * 0.05
        
        # Boost based on context
        if context:
            if intent == 'pest_detection' and context.get('image_data'):
                boost += 0.2
            elif intent == 'risk_assessment' and context.get('location'):
                boost += 0.1
            elif intent == 'crop_recommendation' and context.get('soil_data'):
                boost += 0.15
        
        return min(confidence + boost, 1.0)
    
    def _fallback_classification(self, query: str, context: Dict[str, Any] = None) -> Tuple[str, float]:
        """Fallback classification using enhanced keyword matching"""
        query_lower = query.lower()
        intent_scores = defaultdict(float)
        
        # Enhanced keyword patterns
        patterns = {
            'crop_recommendation': {
                'primary': ['recommend', 'suggest', 'best crop', 'what to plant', 'which crop'],
                'secondary': ['soil', 'climate', 'suitable', 'grow', 'plant', 'farming'],
                'context': ['ph', 'nitrogen', 'phosphorus', 'potassium', 'temperature']
            },
            'market_yield': {
                'primary': ['price', 'market', 'yield', 'forecast', 'predict'],
                'secondary': ['profit', 'revenue', 'cost', 'sell', 'buy', 'trade'],
                'context': ['ton', 'quintal', 'per acre', 'per hectare', 'rupees']
            },
            'risk_assessment': {
                'primary': ['risk', 'danger', 'threat', 'weather risk', 'climate risk'],
                'secondary': ['drought', 'flood', 'storm', 'temperature', 'rainfall'],
                'context': ['probability', 'chance', 'likely', 'forecast', 'warning']
            },
            'pest_detection': {
                'primary': ['pest', 'bug', 'disease', 'identify', 'what is this'],
                'secondary': ['insect', 'fungal', 'bacterial', 'infection', 'damage'],
                'context': ['leaf', 'plant', 'crop', 'treatment', 'control']
            },
            'finance_agent': {
                'primary': ['loan', 'credit', 'subsidy', 'scheme', 'financial'],
                'secondary': ['cost', 'budget', 'money', 'investment', 'insurance'],
                'context': ['bank', 'government', 'interest', 'EMI', 'premium']
            }
        }
        
        # Score each intent
        for intent, keywords in patterns.items():
            score = 0
            
            # Primary keywords (high weight)
            for keyword in keywords['primary']:
                if keyword in query_lower:
                    score += 3
            
            # Secondary keywords (medium weight)
            for keyword in keywords['secondary']:
                if keyword in query_lower:
                    score += 2
            
            # Context keywords (low weight)
            for keyword in keywords['context']:
                if keyword in query_lower:
                    score += 1
            
            if score > 0:
                intent_scores[intent] = score / (len(keywords['primary']) * 3 + 
                                               len(keywords['secondary']) * 2 + 
                                               len(keywords['context']))
        
        if not intent_scores:
            return 'general', 0.4
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent], 0.8)  # Cap fallback confidence
        
        return best_intent, confidence
    
    def extract_parameters(self, query: str, intent: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract comprehensive parameters from query using NLP and pattern matching
        
        Args:
            query: User query
            intent: Classified intent
            context: Additional context
            
        Returns:
            Dictionary of extracted parameters
        """
        params = {'query': query, 'intent': intent}
        
        # Add context data
        if context:
            params.update(context)
        
        # Intent-specific parameter extraction
        if intent == 'crop_recommendation':
            params.update(self._extract_crop_recommendation_params(query))
        elif intent == 'market_yield':
            params.update(self._extract_market_yield_params(query))
        elif intent == 'risk_assessment':
            params.update(self._extract_risk_assessment_params(query))
        elif intent == 'pest_detection':
            params.update(self._extract_pest_detection_params(query))
        elif intent == 'finance_agent':
            params.update(self._extract_finance_params(query))
        
        # Common parameter extraction
        params.update(self._extract_common_params(query))
        
        return params
    
    def _extract_crop_recommendation_params(self, query: str) -> Dict[str, Any]:
        """Extract parameters specific to crop recommendation"""
        params = {}
        query_lower = query.lower()
        
        # Soil parameters
        soil_params = self._extract_soil_parameters(query_lower)
        params.update(soil_params)
        
        # Climate parameters
        climate_params = self._extract_climate_parameters(query_lower)
        params.update(climate_params)
        
        # Area information
        area_info = self._extract_area_information(query_lower)
        params.update(area_info)
        
        # Farming type
        farming_type = self._extract_farming_type(query_lower)
        if farming_type:
            params['farming_type'] = farming_type
        
        return params
    
    def _extract_market_yield_params(self, query: str) -> Dict[str, Any]:
        """Extract parameters for market and yield predictions"""
        params = {}
        query_lower = query.lower()
        
        # Crop identification
        crop = self._extract_crop_name(query_lower)
        if crop:
            params['crop'] = crop
        
        # Time frame
        timeframe = self._extract_timeframe(query_lower)
        if timeframe:
            params['timeframe'] = timeframe
        
        # Quantity/Area
        quantity = self._extract_quantity(query_lower)
        if quantity:
            params.update(quantity)
        
        # Market type
        market_type = self._extract_market_type(query_lower)
        if market_type:
            params['market_type'] = market_type
        
        return params
    
    def _extract_risk_assessment_params(self, query: str) -> Dict[str, Any]:
        """Extract parameters for risk assessment"""
        params = {}
        query_lower = query.lower()
        
        # Risk types
        risk_types = self._extract_risk_types(query_lower)
        if risk_types:
            params['risk_types'] = risk_types
        
        # Location
        location = self._extract_location(query_lower)
        if location:
            params['location'] = location
        
        # Time period
        time_period = self._extract_time_period(query_lower)
        if time_period:
            params['time_period'] = time_period
        
        return params
    
    def _extract_pest_detection_params(self, query: str) -> Dict[str, Any]:
        """Extract parameters for pest detection"""
        params = {}
        query_lower = query.lower()
        
        # Crop type
        crop = self._extract_crop_name(query_lower)
        if crop:
            params['crop_type'] = crop
        
        # Symptoms
        symptoms = self._extract_symptoms(query_lower)
        if symptoms:
            params['symptoms'] = symptoms
        
        # Affected parts
        affected_parts = self._extract_affected_parts(query_lower)
        if affected_parts:
            params['affected_parts'] = affected_parts
        
        return params
    
    def _extract_finance_params(self, query: str) -> Dict[str, Any]:
        """Extract parameters for financial queries"""
        params = {}
        query_lower = query.lower()
        
        # Loan amount
        amount = self._extract_monetary_amount(query_lower)
        if amount:
            params['amount'] = amount
        
        # Loan type
        loan_type = self._extract_loan_type(query_lower)
        if loan_type:
            params['loan_type'] = loan_type
        
        # Purpose
        purpose = self._extract_financial_purpose(query_lower)
        if purpose:
            params['purpose'] = purpose
        
        return params
    
    def _extract_common_params(self, query: str) -> Dict[str, Any]:
        """Extract common parameters from any query"""
        params = {}
        query_lower = query.lower()
        
        # Location
        location = self._extract_location(query_lower)
        if location:
            params['location'] = location
        
        # Numbers
        numbers = self.parameter_extractors['numbers'].findall(query)
        if numbers:
            params['numbers'] = [float(n) for n in numbers]
        
        return params
    
    # Helper methods for parameter extraction
    def _extract_soil_parameters(self, query: str) -> Dict[str, Any]:
        """Extract soil-related parameters"""
        params = {}
        
        # pH extraction
        ph_patterns = [
            r'ph\s*(?:is|of|=|:)?\s*(\d+\.?\d*)',
            r'acidity\s*(?:is|of|=|:)?\s*(\d+\.?\d*)',
            r'alkalinity\s*(?:is|of|=|:)?\s*(\d+\.?\d*)'
        ]
        
        for pattern in ph_patterns:
            match = re.search(pattern, query)
            if match:
                params['ph'] = float(match.group(1))
                break
        
        # NPK extraction
        for nutrient, keywords in self.parameter_extractors['soil_nutrients'].items():
            for keyword in keywords:
                pattern = f'{keyword}\\s*(?:is|of|=|:)?\\s*(\\d+\\.?\\d*)'
                match = re.search(pattern, query)
                if match:
                    params[nutrient[0].upper()] = float(match.group(1))
                    break
        
        # Soil type
        soil_types = ['clay', 'sandy', 'loam', 'silt', 'peat', 'chalk', 'saline']
        for soil_type in soil_types:
            if soil_type in query:
                params['soil_type'] = soil_type
                break
        
        return params
    
    def _extract_climate_parameters(self, query: str) -> Dict[str, Any]:
        """Extract climate-related parameters"""
        params = {}
        
        # Temperature
        temp_patterns = [
            r'temperature\s*(?:is|of|=|:)?\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:degrees?|°)\s*(?:celsius|c)',
            r'(\d+\.?\d*)\s*(?:degrees?|°)\s*(?:fahrenheit|f)'
        ]
        
        for pattern in temp_patterns:
            match = re.search(pattern, query)
            if match:
                temp = float(match.group(1))
                # Convert Fahrenheit to Celsius if needed
                if 'fahrenheit' in pattern or '°f' in pattern:
                    temp = (temp - 32) * 5/9
                params['temperature'] = temp
                break
        
        # Humidity
        humidity_match = re.search(r'humidity\s*(?:is|of|=|:)?\s*(\d+\.?\d*)', query)
        if humidity_match:
            params['humidity'] = float(humidity_match.group(1))
        
        # Rainfall
        rainfall_patterns = [
            r'rainfall\s*(?:is|of|=|:)?\s*(\d+\.?\d*)',
            r'precipitation\s*(?:is|of|=|:)?\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:mm|millimeter|inch|in)\s*(?:rain|rainfall)'
        ]
        
        for pattern in rainfall_patterns:
            match = re.search(pattern, query)
            if match:
                params['rainfall'] = float(match.group(1))
                break
        
        return params
    
    def _extract_crop_name(self, query: str) -> Optional[str]:
        """Extract crop name from query"""
        for crop in self.parameter_extractors['crops']:
            if crop in query:
                return crop
        return None
    
    def _extract_location(self, query: str) -> Optional[str]:
        """Extract location from query"""
        match = self.parameter_extractors['locations'].search(query)
        if match:
            return match.group(1).strip()
        
        # Fallback patterns
        location_patterns = [
            r'(?:in|at|near|around)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:area|region|district|state)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, query)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_timeframe(self, query: str) -> Optional[Dict[str, Any]]:
        """Extract timeframe information"""
        timeframe_patterns = {
            r'(\d+)\s*days?': {'value': lambda x: int(x), 'unit': 'days'},
            r'(\d+)\s*weeks?': {'value': lambda x: int(x), 'unit': 'weeks'},
            r'(\d+)\s*months?': {'value': lambda x: int(x), 'unit': 'months'},
            r'next\s*week': {'value': lambda x: 1, 'unit': 'weeks'},
            r'next\s*month': {'value': lambda x: 1, 'unit': 'months'},
            r'this\s*season': {'value': lambda x: 1, 'unit': 'seasons'},
            r'next\s*season': {'value': lambda x: 1, 'unit': 'seasons'}
        }
        
        for pattern, config in timeframe_patterns.items():
            match = re.search(pattern, query)
            if match:
                if match.groups():
                    value = config['value'](match.group(1))
                else:
                    value = config['value'](None)
                return {'value': value, 'unit': config['unit']}
        
        return None
    
    def _extract_area_information(self, query: str) -> Dict[str, Any]:
        """Extract area/land information"""
        params = {}
        
        area_patterns = [
            r'(\d+\.?\d*)\s*(?:acres?|acre)',
            r'(\d+\.?\d*)\s*(?:hectares?|hectare|ha)',
            r'(\d+\.?\d*)\s*(?:sq\s*ft|square\s*feet)',
            r'(\d+\.?\d*)\s*(?:sq\s*m|square\s*meter)'
        ]
        
        for pattern in area_patterns:
            match = re.search(pattern, query)
            if match:
                area_value = float(match.group(1))
                if 'acre' in pattern:
                    params['area_acres'] = area_value
                elif 'hectare' in pattern or 'ha' in pattern:
                    params['area_hectares'] = area_value
                elif 'sq ft' in pattern or 'square feet' in pattern:
                    params['area_sqft'] = area_value
                elif 'sq m' in pattern or 'square meter' in pattern:
                    params['area_sqm'] = area_value
                break
        
        return params
    
    def _extract_farming_type(self, query: str) -> Optional[str]:
        """Extract farming type"""
        farming_types = [
            'organic', 'conventional', 'hydroponic', 'greenhouse', 
            'polyhouse', 'drip irrigation', 'sprinkler', 'traditional'
        ]
        
        for farming_type in farming_types:
            if farming_type in query:
                return farming_type
        
        return None
    
    def _extract_quantity(self, query: str) -> Dict[str, Any]:
        """Extract quantity information"""
        params = {}
        
        quantity_patterns = [
            r'(\d+\.?\d*)\s*(?:tons?|tonne)',
            r'(\d+\.?\d*)\s*(?:quintals?|qtl)',
            r'(\d+\.?\d*)\s*(?:kg|kilograms?)',
            r'(\d+\.?\d*)\s*(?:bags?)',
            r'(\d+\.?\d*)\s*(?:sacks?)'
        ]
        
        for pattern in quantity_patterns:
            match = re.search(pattern, query)
            if match:
                quantity_value = float(match.group(1))
                if 'ton' in pattern:
                    params['quantity_tons'] = quantity_value
                elif 'quintal' in pattern or 'qtl' in pattern:
                    params['quantity_quintals'] = quantity_value
                elif 'kg' in pattern:
                    params['quantity_kg'] = quantity_value
                elif 'bag' in pattern:
                    params['quantity_bags'] = quantity_value
                elif 'sack' in pattern:
                    params['quantity_sacks'] = quantity_value
                break
        
        return params
    
    def _extract_market_type(self, query: str) -> Optional[str]:
        """Extract market type"""
        market_types = ['wholesale', 'retail', 'mandi', 'local', 'export', 'domestic']
        
        for market_type in market_types:
            if market_type in query:
                return market_type
        
        return None
    
    def _extract_risk_types(self, query: str) -> List[str]:
        """Extract risk types"""
        risk_types = []
        
        risk_keywords = {
            'drought': ['drought', 'dry', 'water shortage', 'no rain'],
            'flood': ['flood', 'flooding', 'too much rain', 'waterlogging'],
            'pest': ['pest', 'insect', 'bug', 'infestation'],
            'disease': ['disease', 'fungal', 'bacterial', 'viral', 'infection'],
            'weather': ['weather', 'climate', 'temperature', 'storm', 'cyclone'],
            'market': ['market', 'price', 'demand', 'supply'],
            'financial': ['financial', 'economic', 'cost', 'profit', 'loss']
        }
        
        for risk_type, keywords in risk_keywords.items():
            if any(keyword in query for keyword in keywords):
                risk_types.append(risk_type)
        
        return risk_types
    
    def _extract_time_period(self, query: str) -> Optional[str]:
        """Extract time period for risk assessment"""
        time_periods = [
            'today', 'tomorrow', 'this week', 'next week', 
            'this month', 'next month', 'this season', 'next season',
            'short term', 'long term', 'immediate'
        ]
        
        for period in time_periods:
            if period in query:
                return period
        
        return None
    
    def _extract_symptoms(self, query: str) -> List[str]:
        """Extract pest/disease symptoms"""
        symptoms = []
        
        symptom_keywords = [
            'yellowing', 'browning', 'wilting', 'spots', 'holes',
            'curling', 'stunted', 'discoloration', 'rotting', 'drying'
        ]
        
        for symptom in symptom_keywords:
            if symptom in query:
                symptoms.append(symptom)
        
        return symptoms
    
    def _extract_affected_parts(self, query: str) -> List[str]:
        """Extract affected plant parts"""
        parts = []
        
        plant_parts = [
            'leaves', 'stem', 'roots', 'flowers', 'fruits',
            'branches', 'trunk', 'seeds', 'pods'
        ]
        
        for part in plant_parts:
            if part in query:
                parts.append(part)
        
        return parts
    
    def _extract_monetary_amount(self, query: str) -> Optional[float]:
        """Extract monetary amounts"""
        amount_patterns = [
            r'(?:rs|rupees?)\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:rs|rupees?)',
            r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakhs?|lakh)',
            r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:crores?|crore)'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, query)
            if match:
                amount_str = match.group(1).replace(',', '')
                amount = float(amount_str)
                
                if 'lakh' in pattern:
                    amount *= 100000
                elif 'crore' in pattern:
                    amount *= 10000000
                
                return amount
        
        return None
    
    def _extract_loan_type(self, query: str) -> Optional[str]:
        """Extract loan type"""
        loan_types = [
            'crop loan', 'kisan credit card', 'kcc', 'term loan',
            'equipment loan', 'land purchase loan', 'working capital'
        ]
        
        for loan_type in loan_types:
            if loan_type in query:
                return loan_type
        
        return None
    
    def _extract_financial_purpose(self, query: str) -> Optional[str]:
        """Extract financial purpose"""
        purposes = [
            'seeds', 'fertilizer', 'pesticide', 'equipment', 'machinery',
            'irrigation', 'land', 'storage', 'processing', 'marketing'
        ]
        
        for purpose in purposes:
            if purpose in query:
                return purpose
        
        return None

    # Legacy methods for backward compatibility
    def predict_intent(self, text: str) -> str:
        """Legacy method for backward compatibility"""
        intent, confidence = self.classify_intent(text)
        return intent

# Create global instance
try:
    intent_classifier = AdvancedIntentClassifier()
    logger.info("Advanced intent classifier initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize intent classifier: {e}")
    intent_classifier = None
    intent_classifier = None