#!/usr/bin/env python3
"""
Test script for multilingual crop recommendation handling
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from orchestrator.orchestrator import Orchestrator

def test_multilingual_crop_recommendation():
    """Test the multilingual crop recommendation fixes"""
    
    print("🧪 Testing Multilingual Crop Recommendation Fixes")
    print("=" * 60)
    
    # Initialize orchestrator
    orch = Orchestrator()
    
    # Test cases
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
            "name": "Parameter Variation (rainfall vs rain)",
            "text": "Recommend a crop",
            "context": {"N": 90, "P": 42, "K": 43, "temperature": 26, "humidity": 80, "ph": 6.5, "rainfall": 200}
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
        print(f"   Context: {test_case['context']}")
        
        try:
            result = orch.handle_query(test_case['text'], test_case['context'])
            
            print(f"   ✅ Language: {result.get('language', 'unknown')}")
            print(f"   ✅ Intent: {result.get('intent', 'unknown')} (confidence: {result.get('confidence', 0):.2f})")
            print(f"   ✅ Agent Used: {result.get('agent_used', 'unknown')}")
            print(f"   ✅ Success: {result.get('success', False)}")
            
            if result.get('success') and 'result' in result:
                crop = result['result'].get('top_crop', 'unknown')
                print(f"   ✅ Recommended Crop: {crop}")
            
            if result.get('answer'):
                print(f"   ✅ Answer: {result['answer'][:100]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_multilingual_crop_recommendation()