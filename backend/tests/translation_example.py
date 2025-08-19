#!/usr/bin/env python3
"""
Example usage of the mT5 translation implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.translation import translate, detect_language

def main():
    """Example usage of translation functions"""
    
    # Example 1: Basic translation
    text = "The crops are growing well this season."
    translated = translate(text, "es")  # Translate to Spanish
    print(f"Original: {text}")
    print(f"Spanish: {translated}")
    
    # Example 2: Language detection
    spanish_text = "Los cultivos están creciendo bien esta temporada."
    detected_lang = detect_language(spanish_text)
    print(f"\nDetected language: {detected_lang}")
    
    # Example 3: Translate back to English
    back_to_english = translate(spanish_text, "en")
    print(f"Back to English: {back_to_english}")
    
    # Example 4: Multiple languages
    original = "Agricultural AI can help farmers make better decisions."
    languages = ["es", "fr", "pt", "hi"]
    
    print(f"\nOriginal: {original}")
    for lang in languages:
        translated = translate(original, lang)
        print(f"{lang.upper()}: {translated}")

if __name__ == "__main__":
    main()