#!/usr/bin/env python3
"""
Test script for the mT5 translation implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.translation import translate, detect_language, translation_service

def test_translation():
    """Test the translation functionality"""
    
    print("Testing mT5 Translation Implementation")
    print("=" * 50)
    
    # Test language detection
    test_texts = [
        "Hello, how are you today?",
        "Hola, ¿cómo estás hoy?",
        "Bonjour, comment allez-vous aujourd'hui?",
        "Olá, como você está hoje?",
        "नमस्ते, आज आप कैसे हैं?"
    ]
    
    print("\n1. Testing Language Detection:")
    print("-" * 30)
    for text in test_texts:
        detected = detect_language(text)
        print(f"Text: '{text[:30]}...' -> Language: {detected}")
    
    # Test translation
    print("\n2. Testing Translation:")
    print("-" * 30)
    
    english_text = "The weather is very good today for farming."
    target_languages = ["es", "fr", "pt", "hi"]
    
    for lang in target_languages:
        try:
            translated = translate(english_text, lang)
            print(f"EN -> {lang.upper()}: '{translated}'")
        except Exception as e:
            print(f"EN -> {lang.upper()}: Error - {e}")
    
    # Test with the service directly
    print("\n3. Testing Translation Service:")
    print("-" * 30)
    
    spanish_text = "El clima está muy bueno hoy para la agricultura."
    try:
        translated_to_english = translation_service.translate_text(spanish_text, "en")
        print(f"ES -> EN: '{translated_to_english}'")
    except Exception as e:
        print(f"ES -> EN: Error - {e}")
    
    print("\n4. Testing Supported Languages:")
    print("-" * 30)
    supported = translation_service.get_supported_languages()
    for code, name in supported.items():
        print(f"{code}: {name}")

if __name__ == "__main__":
    test_translation()