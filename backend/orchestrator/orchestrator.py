import os, json
import logging
from langdetect import detect, LangDetectException
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Handle googletrans import gracefully for Python 3.13 compatibility
try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"googletrans not available: {e}. Translation features will be limited.")
    Translator = None
    GOOGLETRANS_AVAILABLE = False

from .intent_classifier import intent_classifier

# Handle relative imports
try:
    from ..agents.base_agent import load_agent_classes
    from ..utils.translation import translation_service
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from agents.base_agent import load_agent_classes
    from utils.translation import translation_service

class Orchestrator:
    def __init__(self, models_dir=None):
        # Handle both new and legacy initialization
        base = os.path.dirname(os.path.dirname(__file__))
        self.models_dir = models_dir or os.path.join(base, "models")
        
        self.translator = Translator() if GOOGLETRANS_AVAILABLE else None
        
        # Load agents
        self.agents = self._load_agents(self.models_dir)
        
        # Lazy load intent classifier (support both advanced and simple)
        try:
            self.intent_clf = intent_classifier  # Use the advanced classifier
        except:
            # Fallback to simple classifier
            from .intent_classifier import IntentClassifier
            self.intent_clf = IntentClassifier()
        
        # Path for simple cache (daily sync)
        self.cache_file = os.path.join(self.models_dir, "daily_cache.json")
        if not os.path.exists(self.cache_file):
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, "w") as f:
                json.dump({}, f)

    def _load_agents(self, models_dir: str) -> Dict[str, Any]:
        """Load and initialize all agents"""
        try:
            agents = load_agent_classes(models_dir)
            logger.info(f"Loaded {len(agents)} agents: {list(agents.keys())}")
            return agents
        except Exception as e:
            logger.error(f"Error loading agents: {e}")
            return {}

    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        try:
            lang = detect(text)
            logger.debug(f"Detected language: {lang}")
            return lang
        except LangDetectException:
            logger.warning("Language detection failed, defaulting to English")
            return "en"

    def to_en(self, text: str, src: Optional[str] = None) -> str:
        """Translate text to English"""
        try:
            if src is None:
                src = self.detect_language(text)
            if src == "en":
                return text
            
            # Use the translation service if available
            if GOOGLETRANS_AVAILABLE:
                translated = translation_service.translate_text(text, 'en', src)
                logger.debug(f"Translated '{text}' from {src} to English: '{translated}'")
                return translated
            else:
                logger.warning("Translation service not available, returning original text")
                return text
        except Exception as e:
            logger.error(f"Translation to English failed: {e}")
            return text

    def to_english(self, text: str, src_lang: str) -> str:
        """Legacy method - placeholder for translation"""
        # For now we assume input in English or the agents accept English-like inputs
        return text

    def from_en(self, text_en: str, dest_lang: str = "en") -> str:
        """Translate text from English to target language"""
        try:
            if dest_lang == "en":
                return text_en
            
            # Use the translation service if available
            if GOOGLETRANS_AVAILABLE:
                translated = translation_service.translate_text(text_en, dest_lang, 'en')
                logger.debug(f"Translated '{text_en}' from English to {dest_lang}: '{translated}'")
                return translated
            else:
                logger.warning("Translation service not available, returning English text")
                return text_en
        except Exception as e:
            logger.error(f"Translation from English failed: {e}")
            return text_en

    def nlg_template(self, intent: str, result: Dict[str, Any]) -> str:
        """Simple templates per intent (English)"""
        if intent == "crop" or intent == "crop_recommendation":
            crop = result.get("top_crop") or result.get("recommended_crops") or result.get("recommendation") or "a suitable crop"
            if isinstance(crop, list) and crop:
                crop = crop[0]
            return f"Recommended crop: {crop}."
        
        if intent == "market_yield":
            price = result.get("predicted_price") or result.get("predicted_price_per_quintal")
            yld = result.get("estimated_yield") or result.get("yield")
            if price and yld:
                return f"Expected yield: {yld}. Predicted price: {price}."
            elif price:
                return f"Predicted price: {price}."
            elif yld:
                return f"Expected yield: {yld}."
            else:
                return "Market analysis completed."
        
        if intent == "risk" or intent == "risk_assessment":
            p = result.get("pest_probability") or result.get("pest_outbreak_probability") or result.get("risk_level")
            adv = result.get("advice", "Monitor crops.")
            if p:
                return f"Risk level: {p}. Advice: {adv}"
            else:
                return f"Advice: {adv}"
        
        if intent == "finance" or intent == "finance_agent":
            schemes = result.get("eligible_schemes", [])
            if schemes:
                return f"Eligible schemes: {', '.join(schemes)}"
            else:
                return "Financial information processed."
        
        if intent == "pest_detection":
            pest = result.get("detected_pest") or result.get("pest_type")
            confidence = result.get("confidence", "")
            if pest:
                return f"Detected pest: {pest}. Confidence: {confidence}"
            else:
                return "Pest analysis completed."
        
        # fallback - try to extract meaningful info
        if isinstance(result, dict):
            if 'message' in result:
                return result['message']
            elif 'recommendation' in result:
                return f"Recommendation: {result['recommendation']}"
            elif 'prediction' in result:
                return f"Prediction: {result['prediction']}"
        
        return str(result)

    def handle_query_simple(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simple query handler matching the original specification"""
        context = context or {}
        lang = self.detect_language(text)
        text_en = self.to_english(text, lang)
        
        # Get intent using the classifier
        if hasattr(self.intent_clf, 'predict_intent'):
            intent = self.intent_clf.predict_intent(text_en)
        else:
            intent, _ = self.intent_clf.classify_intent(text_en, context)
        
        agent = self.agents.get(intent)
        if not agent:
            # fallback to crop
            agent = self.agents.get("crop")
        
        # payload for the agent: include text_en and context
        payload = {"text": text_en, "context": context}
        result = agent.predict(payload) if agent else {"error": "No agent available"}
        
        # produce short answer via template
        answer_en = self.nlg_template(intent, result)
        
        # we will integrate translation back to user's language later
        answer_local = answer_en  # placeholder
        
        return {
            "language": lang,
            "intent": intent,
            "source_agent": agent.name if agent else None,
            "result": result,
            "answer": answer_local
        }

    def handle_query(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle user query with advanced intent classification and parameter extraction
        
        Args:
            text: User query text
            context: Additional context (image data, location, etc.)
            
        Returns:
            Comprehensive response with results and metadata
        """
        if context is None:
            context = {}
            
        try:
            # 1) Detect language and translate to English
            lang = self.detect_language(text)
            text_en = self.to_en(text, src=lang)
            
            logger.info(f"Language detected: {lang}")
            if lang != 'en':
                logger.info(f"Original query: {text}")
                logger.info(f"Translated query: {text_en}")
            
            # 2) Advanced intent classification with confidence
            intent, confidence = self.intent_clf.classify_intent(text_en, context)
            logger.info(f"Classified intent: {intent} (confidence: {confidence:.2f})")
            
            # 3) Extract comprehensive parameters
            parameters = self.intent_clf.extract_parameters(text_en, intent, context)
            logger.debug(f"Extracted parameters: {parameters}")
            
            # 4) Prepare enhanced payload
            payload = {
                "text": text_en,
                "original_text": text,
                "language": lang,
                "intent": intent,
                "confidence": confidence,
                "parameters": parameters,
                "context": context
            }
            
            # 5) Route to appropriate agent
            logger.info(f"Routing intent '{intent}' (confidence: {confidence:.2f}) with parameters: {list(parameters.keys())}")
            agent_result = self._route_to_agent(intent, payload)
            
            # 6) Generate natural language response using mT5
            if lang != "en" and agent_result.get('success', False):
                # Use mT5 to generate natural response in user's language
                natural_answer = translation_service.generate_natural_response(
                    agent_result, intent, lang, text
                )
            else:
                # For English or failed requests, use simple response generation
                natural_answer = self._generate_simple_answer(agent_result, intent)
            
            # 7) Generate comprehensive response
            response = self._generate_response(
                agent_result, intent, lang, confidence, parameters, context, natural_answer
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error handling query: {e}")
            return self._generate_error_response(str(e), lang if 'lang' in locals() else 'en')

    def _route_to_agent(self, intent: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Route query to appropriate agent based on intent"""
        try:
            # Map intents to agent names
            intent_to_agent = {
                'crop_recommendation': 'crop',
                'market_yield': 'market_yield',
                'risk_assessment': 'risk',
                'pest_detection': 'pest',
                'finance_agent': 'finance'
            }
            
            agent_name = intent_to_agent.get(intent)
            
            # Force routing to crop agent for crop_recommendation intent (bypass confidence threshold)
            if intent == 'crop_recommendation':
                agent_name = 'crop'
                logger.info(f"Forcing route to crop agent for crop_recommendation intent (confidence: {payload['confidence']:.2f})")
            
            if agent_name and agent_name in self.agents:
                agent = self.agents[agent_name]
                logger.info(f"Routing to agent: {agent_name}")
                
                # Normalize parameters for crop agent
                if agent_name == 'crop':
                    context = payload.get('context', {})
                    parameters = payload.get('parameters', {})
                    
                    # Merge parameters into context for crop agent
                    for key, value in parameters.items():
                        if key not in context and value is not None:
                            context[key] = value
                    
                    # Normalize parameter names to match ML model expectations
                    # Model expects: ["N", "P", "K", "temperature", "humidity", "ph", "rain"]
                    param_mapping = {
                        'rainfall': 'rain',
                        'nitrogen': 'N',
                        'phosphorus': 'P', 
                        'potassium': 'K',
                        'temp': 'temperature',
                        'pH': 'ph'
                    }
                    
                    for old_key, new_key in param_mapping.items():
                        if old_key in context and new_key not in context:
                            context[new_key] = context[old_key]
                            logger.debug(f"Normalized parameter: {old_key} -> {new_key}")
                    
                    # Also ensure reverse mapping for compatibility
                    if 'rain' in context and 'rainfall' not in context:
                        context['rainfall'] = context['rain']
                    
                    payload['context'] = context
                    logger.debug(f"Normalized context for crop agent: {context}")
                
                # Call agent with enhanced payload
                if hasattr(agent, 'process_query'):
                    result = agent.process_query(payload['text'], payload)
                else:
                    # Fallback for older agent interface
                    result = agent.predict(payload)
                
                result['agent_used'] = agent_name
                result['agent_confidence'] = payload['confidence']
                
                return result
                
            else:
                # Handle unknown intents or missing agents
                logger.warning(f"No agent found for intent: {intent}")
                return self._handle_general_query(payload)
                
        except Exception as e:
            logger.error(f"Error routing to agent: {e}")
            return {
                'error': f"Agent processing failed: {str(e)}",
                'agent_used': None,
                'success': False
            }

    def _handle_general_query(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general queries that don't fit specific intents"""
        text = payload['text'].lower()
        parameters = payload.get('parameters', {})
        
        # Try to provide helpful general responses
        if any(word in text for word in ['help', 'what can you do', 'capabilities']):
            return {
                'message': """I can help you with:
                1. Crop recommendations based on soil and climate
                2. Market price and yield predictions
                3. Weather and agricultural risk assessment
                4. Pest and disease identification
                5. Agricultural finance and loan information
                
                Please ask me about any of these topics!""",
                'agent_used': 'general',
                'success': True,
                'suggestions': [
                    "What crop should I plant?",
                    "Predict wheat prices",
                    "Assess drought risk",
                    "Identify this pest",
                    "Agricultural loan options"
                ]
            }
        
        # Try to route based on extracted parameters
        if parameters.get('crop'):
            # If crop is mentioned, try crop agent
            if 'crop' in self.agents:
                return self.agents['crop'].process_query(payload['text'], payload)
        
        # Default response
        return {
            'message': "I'm not sure how to help with that specific query. Could you please ask about crop recommendations, market prices, risk assessment, pest identification, or agricultural finance?",
            'agent_used': 'general',
            'success': False,
            'suggestions': [
                "Try asking: 'What crop should I plant in sandy soil?'",
                "Or: 'What will be the price of rice next month?'",
                "Or: 'What are the weather risks for my crops?'"
            ]
        }

    def _generate_simple_answer(self, agent_result: Dict[str, Any], intent: str) -> str:
        """Generate simple English answer from agent result"""
        if 'message' in agent_result:
            return agent_result['message']
        elif intent == 'crop_recommendation':
            crop = agent_result.get('top_crop', 'a suitable crop')
            return f"I recommend growing {crop} based on your conditions."
        elif intent == 'market_yield':
            return "Here's the market and yield analysis for your query."
        elif intent == 'risk_assessment':
            return "I've analyzed the agricultural risks for your situation."
        elif intent == 'pest_detection':
            return "I've identified potential pest issues in your image."
        elif intent == 'finance_agent':
            return "Here's information about agricultural financing options."
        else:
            return "I've processed your agricultural query."

    def _generate_response(self, agent_result: Dict[str, Any], intent: str, 
                         language: str, confidence: float, 
                         parameters: Dict[str, Any], context: Dict[str, Any], 
                         natural_answer: str = None) -> Dict[str, Any]:
        """Generate comprehensive response"""
        
        response = {
            'success': agent_result.get('success', True),
            'language': language,
            'intent': intent,
            'confidence': confidence,
            'agent_used': agent_result.get('agent_used'),
            'parameters': parameters,
            'result': agent_result,
            'timestamp': self._get_timestamp()
        }
        
        # Add main message/answer (use natural answer if provided)
        if natural_answer:
            response['answer'] = natural_answer
        elif 'message' in agent_result:
            response['answer'] = agent_result['message']
        elif 'recommendations' in agent_result:
            response['answer'] = self._format_recommendations(agent_result['recommendations'])
        elif 'predictions' in agent_result:
            response['answer'] = self._format_predictions(agent_result['predictions'])
        else:
            response['answer'] = "I've processed your request. Please check the detailed results."
        
        # Add suggestions if available
        if 'suggestions' in agent_result:
            response['suggestions'] = agent_result['suggestions']
        
        # Add confidence warning for low confidence predictions
        if confidence < 0.6:
            response['warning'] = "I'm not very confident about this classification. Please verify the results or rephrase your question."
        
        return response

    def _generate_error_response(self, error_message: str, language: str) -> Dict[str, Any]:
        """Generate error response"""
        return {
            'success': False,
            'error': error_message,
            'language': language,
            'answer': "I encountered an error processing your request. Please try again or rephrase your question.",
            'timestamp': self._get_timestamp()
        }

    def _format_recommendations(self, recommendations: Any) -> str:
        """Format crop recommendations into readable text"""
        if isinstance(recommendations, list):
            if len(recommendations) > 0:
                return f"Based on your conditions, I recommend: {', '.join(str(r) for r in recommendations[:3])}"
            else:
                return "No specific recommendations available for your conditions."
        elif isinstance(recommendations, dict):
            if 'recommendations' in recommendations:
                return self._format_recommendations(recommendations['recommendations'])
            else:
                return str(recommendations)
        else:
            return str(recommendations)

    def _format_predictions(self, predictions: Any) -> str:
        """Format predictions into readable text"""
        if isinstance(predictions, dict):
            if 'predicted_price' in predictions:
                return f"Predicted price: {predictions['predicted_price']}"
            elif 'predicted_yield' in predictions:
                return f"Expected yield: {predictions['predicted_yield']}"
            else:
                return str(predictions)
        else:
            return str(predictions)

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    # Enhanced cache utilities
    def update_cache(self, key: str, value: Any):
        """Update cache with new value"""
        try:
            with open(self.cache_file, "r+") as f:
                data = json.load(f)
                data[key] = value
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        except Exception as e:
            logger.error(f"Error updating cache: {e}")

    def read_cache(self, key: str) -> Any:
        """Read value from cache"""
        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
            return data.get(key)
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return None

    def clear_cache(self):
        """Clear all cache data"""
        try:
            with open(self.cache_file, "w") as f:
                json.dump({}, f)
            logger.info("Cache cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all loaded agents"""
        status = {}
        for agent_name, agent in self.agents.items():
            try:
                status[agent_name] = {
                    'loaded': True,
                    'name': getattr(agent, 'name', agent_name),
                    'model_loaded': hasattr(agent, 'model') and agent.model is not None
                }
            except Exception as e:
                status[agent_name] = {
                    'loaded': False,
                    'error': str(e)
                }
        return status


