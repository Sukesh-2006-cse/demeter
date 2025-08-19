#!/usr/bin/env python3
"""
Test Tamil translation directly
"""
import sys
sys.path.append('backend')

from utils.translation import translation_service

def test_tamil_translation():
    print("Testing Tamil translation...")
    
    # Test English to Tamil translation
    english_text = "I suggest growing rice based on your conditions, though you may want to consider other factors as well."
    
    print(f"Original English: {english_text}")
    
    try:
        tamil_translation = translation_service.translate_text(english_text, 'ta', 'en')
        print(f"Tamil Translation: {tamil_translation}")
        
        # Test if Tamil is in supported languages
        print(f"Supported languages: {list(translation_service.supported_languages.keys())}")
        print(f"Tamil supported: {'ta' in translation_service.supported_languages}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tamil_translation()