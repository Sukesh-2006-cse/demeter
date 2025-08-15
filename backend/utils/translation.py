"""
Multilingual translation utilities
"""
import os
from typing import Dict, Any, Optional, List
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# Handle googletrans import gracefully for Python 3.13 compatibility
try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"googletrans not available: {e}. Translation features will be limited.")
    Translator = None
    GOOGLETRANS_AVAILABLE = False

class TranslationService:
    """Service for handling multilingual translations"""
    
    def __init__(self):
        self.translator = Translator() if GOOGLETRANS_AVAILABLE else None
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'pt': 'Portuguese',
            'hi': 'Hindi',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'sw': 'Swahili',
            'am': 'Amharic'
        }
        self.cache = {}
        self.cache_file = Path(__file__).parent.parent / "data" / "translation_cache.json"
        self._load_cache()
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> str:
        """
        Translate text to target language
        
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
        
        # Return original if already in target language
        if source_language == target_language:
            return text
        
        # Check cache first
        cache_key = f"{text}_{source_language}_{target_language}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Perform translation if translator is available
            if self.translator is not None:
                result = self.translator.translate(text, dest=target_language, src=source_language)
                translated_text = result.text
                
                # Cache the result
                self.cache[cache_key] = translated_text
                self._save_cache()
                
                return translated_text
            else:
                logger.warning("Translation service not available, returning original text")
                return text
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original text on error
    
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
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code
        """
        if not text or not text.strip():
            return 'en'
        
        try:
            if self.translator is not None:
                detection = self.translator.detect(text)
                detected_lang = detection.lang
                
                # Return detected language if supported, otherwise default to English
                return detected_lang if detected_lang in self.supported_languages else 'en'
            else:
                logger.warning("Translation service not available, defaulting to English")
                return 'en'
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en'
    
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

# Global instances
translation_service = TranslationService()
localized_responses = LocalizedResponses()