"""
Multilingual translation utilities using mT5 model
"""
import os
from typing import Dict, Any, Optional, List
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# Import required libraries for mT5 translation
try:
    from transformers import MT5ForConditionalGeneration, MT5Tokenizer
    from langdetect import detect
    MT5_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Required libraries not available: {e}. Translation features will be limited.")
    MT5ForConditionalGeneration = None
    MT5Tokenizer = None
    detect = None
    MT5_AVAILABLE = False

# Fallback to googletrans if mT5 is not available
try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"googletrans not available: {e}. Translation features will be limited.")
    Translator = None
    GOOGLETRANS_AVAILABLE = False

class TranslationService:
    """Service for handling multilingual translations using mT5 model"""
    
    def __init__(self):
        self.mt5_model = None
        self.mt5_tokenizer = None
        self.fallback_translator = Translator() if GOOGLETRANS_AVAILABLE else None
        
        # Initialize mT5 model
        if MT5_AVAILABLE:
            try:
                model_name = "google/mt5-small"
                logger.info(f"Loading mT5 model: {model_name}")
                self.mt5_tokenizer = MT5Tokenizer.from_pretrained(model_name)
                self.mt5_model = MT5ForConditionalGeneration.from_pretrained(model_name)
                logger.info("mT5 model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load mT5 model: {e}")
                self.mt5_model = None
                self.mt5_tokenizer = None
        
        self.supported_languages = {
            'en': 'English',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'hi': 'Hindi',
            'fr': 'French',
            'es': 'Spanish',
            'ru': 'Russian'
        }
        self.cache = {}
        self.cache_file = Path(__file__).parent.parent / "data" / "translation_cache.json"
        self._load_cache()
    
    def translate_with_mt5(self, text: str, target_lang: str = "en") -> str:
        """
        Translate text to target language using mT5 model.
        
        Args:
            text: Text to translate
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        if not self.mt5_model or not self.mt5_tokenizer:
            logger.warning("mT5 model not available")
            return text
        
        try:
            # Detect source language
            source_lang = self.detect_language(text)
            
            # Skip translation if already in target language
            if source_lang == target_lang:
                return text
            
            # Create translation task prefix
            task_prefix = f"translate {source_lang} to {target_lang}: "
            
            # Tokenize input
            input_ids = self.mt5_tokenizer(
                task_prefix + text, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True
            ).input_ids
            
            # Generate translation
            outputs = self.mt5_model.generate(
                input_ids, 
                max_length=128, 
                num_beams=4, 
                early_stopping=True,
                do_sample=False
            )
            
            # Decode the output
            translated_text = self.mt5_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up the output (remove task prefix if present)
            if translated_text.startswith(task_prefix):
                translated_text = translated_text[len(task_prefix):].strip()
            
            return translated_text
            
        except Exception as e:
            logger.error(f"mT5 translation error: {e}")
            return text

    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text using langdetect.
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code
        """
        if not text or not text.strip():
            return 'en'
        
        try:
            if detect is not None:
                detected_lang = detect(text)
                # Return detected language if supported, otherwise default to English
                return detected_lang if detected_lang in self.supported_languages else 'en'
            else:
                logger.warning("Language detection not available, defaulting to English")
                return 'en'
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en'

    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> str:
        """
        Translate text to target language using mT5 model with fallback to googletrans
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto-detect if 'auto')
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
        
        # Check if target language is supported
        if target_language not in self.supported_languages:
            logger.warning(f"Unsupported language: {target_language}")
            return text
        
        # Auto-detect source language if needed
        if source_language == 'auto':
            source_language = self.detect_language(text)
        
        # Return original if already in target language
        if source_language == target_language:
            return text
        
        # Check cache first
        cache_key = f"{text}_{source_language}_{target_language}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        translated_text = text
        
        try:
            # Try mT5 translation first
            if self.mt5_model and self.mt5_tokenizer:
                translated_text = self.translate_with_mt5(text, target_language)
                logger.debug(f"Used mT5 for translation: {text[:50]}... -> {translated_text[:50]}...")
            
            # Fallback to googletrans if mT5 fails or is not available
            elif self.fallback_translator is not None:
                result = self.fallback_translator.translate(text, dest=target_language, src=source_language)
                translated_text = result.text
                logger.debug(f"Used googletrans for translation: {text[:50]}... -> {translated_text[:50]}...")
            
            else:
                logger.warning("No translation service available, returning original text")
                return text
            
            # Cache the result
            self.cache[cache_key] = translated_text
            self._save_cache()
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original text on error
    
    def generate_natural_response(self, agent_result: Dict[str, Any], intent: str, target_language: str, original_query: str) -> str:
        """
        Generate natural language response using mT5 based on agent results
        
        Args:
            agent_result: Results from the sub-agent
            intent: The classified intent
            target_language: Target language for response
            original_query: Original user query
            
        Returns:
            Natural language response in target language
        """
        try:
            # Create a structured prompt for mT5 to generate natural response
            if intent == 'crop_recommendation':
                crop = agent_result.get('top_crop', 'unknown crop')
                confidence = agent_result.get('confidence', 0)
                
                # Create English template
                if confidence > 0.7:
                    english_response = f"Based on your soil and climate conditions, I recommend growing {crop}. This recommendation has high confidence."
                elif confidence > 0.5:
                    english_response = f"I suggest growing {crop} based on your conditions, though you may want to consider other factors as well."
                else:
                    english_response = f"Based on basic analysis, {crop} might be suitable for your conditions, but I recommend consulting with local agricultural experts."
                    
            elif intent == 'market_yield':
                price = agent_result.get('predicted_price', 'unknown')
                yield_val = agent_result.get('estimated_yield', 'unknown')
                english_response = f"Expected yield: {yield_val}. Predicted market price: {price}."
                
            elif intent == 'risk_assessment':
                risk_level = agent_result.get('risk_level', 'moderate')
                advice = agent_result.get('advice', 'Monitor your crops regularly.')
                english_response = f"Risk assessment shows {risk_level} risk level. Advice: {advice}"
                
            elif intent == 'pest_detection':
                pest = agent_result.get('detected_pest', 'unknown pest')
                confidence = agent_result.get('confidence', 0)
                english_response = f"Detected pest: {pest} (confidence: {confidence:.1%}). Please take appropriate measures."
                
            elif intent == 'finance_agent':
                schemes = agent_result.get('eligible_schemes', [])
                if schemes:
                    english_response = f"You may be eligible for these financial schemes: {', '.join(schemes[:3])}."
                else:
                    english_response = "I found some general agricultural finance information for you."
            else:
                # Fallback for unknown intents
                english_response = agent_result.get('message', 'I have processed your request.')
            
            # If target language is English, return as is
            if target_language == 'en':
                return english_response
            
            # Use translation service (prioritize googletrans for speed)
            return self.translate_text(english_response, target_language)
                
        except Exception as e:
            logger.error(f"Error generating natural response: {e}")
            # Fallback to translation
            english_fallback = agent_result.get('message', 'I have processed your request.')
            return self.translate_text(english_fallback, target_language)

    def translate_response(self, response: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """
        Translate response dictionary to target language
        
        Args:
            response: Response dictionary to translate
            target_language: Target language code
            
        Returns:
            Translated response dictionary
        """
        if target_language == 'en' or target_language not in self.supported_languages:
            return response
        
        translated_response = response.copy()
        
        # Fields that should be translated
        translatable_fields = [
            'message', 'description', 'error', 'recommendation', 
            'advice', 'summary', 'explanation', 'reason'
        ]
        
        # Translate top-level fields
        for field in translatable_fields:
            if field in translated_response and isinstance(translated_response[field], str):
                translated_response[field] = self.translate_text(
                    translated_response[field], target_language
                )
        
        # Translate nested structures
        translated_response = self._translate_nested(translated_response, target_language)
        
        return translated_response
    
    def _translate_nested(self, obj: Any, target_language: str) -> Any:
        """Recursively translate nested structures"""
        if isinstance(obj, dict):
            translated = {}
            for key, value in obj.items():
                # Translate key if it's a translatable field name
                if key in ['name', 'title', 'label', 'description', 'message']:
                    if isinstance(value, str):
                        translated[key] = self.translate_text(value, target_language)
                    else:
                        translated[key] = self._translate_nested(value, target_language)
                else:
                    translated[key] = self._translate_nested(value, target_language)
            return translated
        
        elif isinstance(obj, list):
            return [self._translate_nested(item, target_language) for item in obj]
        
        elif isinstance(obj, str):
            # Only translate if it looks like natural language (not codes/IDs)
            if len(obj) > 3 and not obj.isupper() and not obj.isdigit():
                return self.translate_text(obj, target_language)
            return obj
        
        else:
            return obj
    

    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported language codes and names"""
        return self.supported_languages.copy()
    
    def _load_cache(self):
        """Load translation cache from file"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
        except Exception as e:
            logger.error(f"Error loading translation cache: {e}")
            self.cache = {}
    
    def _save_cache(self):
        """Save translation cache to file"""
        try:
            # Ensure directory exists
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Limit cache size to prevent it from growing too large
            if len(self.cache) > 10000:
                # Keep only the most recent 5000 entries
                cache_items = list(self.cache.items())
                self.cache = dict(cache_items[-5000:])
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving translation cache: {e}")

class LocalizedResponses:
    """Predefined localized responses for common messages"""
    
    def __init__(self):
        self.responses = {
            'en': {
                'welcome': "Welcome to the Agricultural AI Assistant",
                'processing': "Processing your request...",
                'error': "An error occurred while processing your request",
                'no_data': "No data available for this request",
                'success': "Request processed successfully",
                'invalid_input': "Invalid input provided",
                'model_loading': "Loading AI model...",
                'prediction_complete': "Prediction completed",
                'high_confidence': "High confidence prediction",
                'low_confidence': "Low confidence prediction - please verify results"
            },
            'es': {
                'welcome': "Bienvenido al Asistente de IA Agrícola",
                'processing': "Procesando su solicitud...",
                'error': "Ocurrió un error al procesar su solicitud",
                'no_data': "No hay datos disponibles para esta solicitud",
                'success': "Solicitud procesada exitosamente",
                'invalid_input': "Entrada inválida proporcionada",
                'model_loading': "Cargando modelo de IA...",
                'prediction_complete': "Predicción completada",
                'high_confidence': "Predicción de alta confianza",
                'low_confidence': "Predicción de baja confianza - por favor verifique los resultados"
            },
            'fr': {
                'welcome': "Bienvenue dans l'Assistant IA Agricole",
                'processing': "Traitement de votre demande...",
                'error': "Une erreur s'est produite lors du traitement de votre demande",
                'no_data': "Aucune donnée disponible pour cette demande",
                'success': "Demande traitée avec succès",
                'invalid_input': "Entrée invalide fournie",
                'model_loading': "Chargement du modèle IA...",
                'prediction_complete': "Prédiction terminée",
                'high_confidence': "Prédiction de haute confiance",
                'low_confidence': "Prédiction de faible confiance - veuillez vérifier les résultats"
            },
            'pt': {
                'welcome': "Bem-vindo ao Assistente de IA Agrícola",
                'processing': "Processando sua solicitação...",
                'error': "Ocorreu um erro ao processar sua solicitação",
                'no_data': "Nenhum dado disponível para esta solicitação",
                'success': "Solicitação processada com sucesso",
                'invalid_input': "Entrada inválida fornecida",
                'model_loading': "Carregando modelo de IA...",
                'prediction_complete': "Predição concluída",
                'high_confidence': "Predição de alta confiança",
                'low_confidence': "Predição de baixa confiança - por favor verifique os resultados"
            }
        }
    
    def get_response(self, key: str, language: str = 'en') -> str:
        """Get localized response for a given key and language"""
        if language not in self.responses:
            language = 'en'
        
        return self.responses[language].get(key, self.responses['en'].get(key, key))
    
    def add_response(self, key: str, language: str, text: str):
        """Add a new localized response"""
        if language not in self.responses:
            self.responses[language] = {}
        
        self.responses[language][key] = text

# Standalone functions for direct use (as requested in the original code)
def translate(text: str, target_lang: str = "en") -> str:
    """
    Translate text to target language using mT5 model.
    
    Args:
        text: Text to translate
        target_lang: Target language code (default: "en")
        
    Returns:
        Translated text
    """
    return translation_service.translate_text(text, target_lang)

def detect_language(text: str) -> str:
    """
    Detect language of a given text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Detected language code
    """
    return translation_service.detect_language(text)

# Global instances
translation_service = TranslationService()
localized_responses = LocalizedResponses()