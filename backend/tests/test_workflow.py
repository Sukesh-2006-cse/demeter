#!/usr/bin/env python3
"""
Test script for multilingual workflow to verify translation back to original language
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.orchestrator import Orchestrator
from utils.translation import translation_service

def test_multilingual_workflow():
    """Test the multilingual workflow of the orchestrator"""
    
    print("🧪 Testing Multilingual Workflow")
    print("=" * 60)
    
    # Initialize orchestrator
    orch = Orchestrator()
    
    # Test cases with different languages
    test_cases = [
        {
            "name": "Tamil Query",
            "text": "இந்த பருவத்தில் எந்த பயிர் நடவு செய்ய வேண்டும்?",
            "context": {"N": 90, "P": 42, "K": 43, "temperature": 26, "humidity": 80, "ph": 6.5, "rain": 200}
        },
        {
            "name": "English Query",
            "text": "What crop should I plant this season?",
            "context": {"N": 90, "P": 42, "K": 43, "temperature": 26, "humidity": 80, "ph": 6.5, "rain": 200}
        },
        {
            "name": "Spanish Query",
            "text": "¿Qué cultivo debo plantar?",
            "context": {"N": 90, "P": 42, "K": 43, "temperature": 26, "humidity": 80, "ph": 6.5, "rain": 200}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   Query: {test_case['text']}")
        
        # Step 1: Detect language
        detected_lang = orch.detect_language(test_case['text'])
        print(f"   Detected Language: {detected_lang}")
        
        # Step 2: Translate to English for processing
        text_en = orch.to_en(test_case['text'])
        print(f"   Translated to English: {text_en}")
        
        # Step 3: Process with appropriate agent
        result = orch.handle_query(test_case['text'], test_case['context'])
        
        # Step 4: Check if response is in original language
        response_language = result.get('language', 'unknown')
        response_text = result.get('answer', 'No answer')
        print(f"   Response Language: {response_language}")
        print(f"   Response: {response_text}")
        
        # Verify if response is in the original language
        detected_response_lang = translation_service.detect_language(response_text)
        print(f"   Detected Response Language: {detected_response_lang}")
        print(f"   Original Query Language: {detected_lang}")
        print(f"   Language Match: {detected_response_lang == detected_lang}")
        
        # Translate response to English to verify content
        response_in_english = translation_service.translate_text(response_text, 'en', detected_response_lang)
        print(f"   Response translated to English: {response_in_english}")
        
        # Print full result for debugging
        print("   Full Result:")
        for key, value in result.items():
            if key != 'result':  # Skip the nested result to keep output clean
                print(f"      {key}: {value}")
    
    print("\n" + "=" * 60)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_multilingual_workflow()