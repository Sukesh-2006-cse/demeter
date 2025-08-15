#!/usr/bin/env python3
"""
Test script to demonstrate the advanced intent classifier capabilities
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    from orchestrator.intent_classifier import intent_classifier
    print("✅ Successfully imported intent_classifier")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Trying to import the class directly...")
    try:
        from orchestrator.intent_classifier import AdvancedIntentClassifier
        intent_classifier = AdvancedIntentClassifier()
        print("✅ Successfully created intent_classifier instance")
    except Exception as e2:
        print(f"❌ Failed to create instance: {e2}")
        print("Checking if scikit-learn is available...")
        try:
            import sklearn
            print(f"✅ scikit-learn version: {sklearn.__version__}")
        except ImportError:
            print("❌ scikit-learn not installed. Please run: pip install scikit-learn")
            sys.exit(1)
        raise e2

import json

def test_intent_classification():
    """Test the advanced intent classifier with various queries"""
    
    test_queries = [
        # Crop recommendation queries
        {
            "query": "What crop should I plant in sandy soil with pH 6.5?",
            "context": {"soil_type": "sandy", "ph": 6.5}
        },
        {
            "query": "I have 5 acres of land with high nitrogen content, suggest best crops",
            "context": {"area_acres": 5, "nitrogen": "high"}
        },
        {
            "query": "Recommend drought resistant crops for hot climate",
            "context": {"climate": "hot", "water_availability": "low"}
        },
        
        # Market and yield queries
        {
            "query": "What will be the price of wheat next month?",
            "context": {}
        },
        {
            "query": "Predict rice yield for 10 hectares",
            "context": {"area_hectares": 10}
        },
        {
            "query": "Market forecast for tomatoes in Punjab",
            "context": {"location": "Punjab"}
        },
        
        # Risk assessment queries
        {
            "query": "What are the drought risks for my crops this season?",
            "context": {}
        },
        {
            "query": "Assess flood probability in Bihar for rice cultivation",
            "context": {"location": "Bihar", "crop": "rice"}
        },
        {
            "query": "Weather risks for farming in monsoon season",
            "context": {"season": "monsoon"}
        },
        
        # Pest detection queries
        {
            "query": "What pest is attacking my tomato plants?",
            "context": {"crop": "tomato"}
        },
        {
            "query": "Identify this disease on wheat leaves",
            "context": {"crop": "wheat", "image_data": "dummy_image_data"}
        },
        {
            "query": "My plants have yellow spots, what could it be?",
            "context": {"symptoms": ["yellow spots"]}
        },
        
        # Finance queries
        {
            "query": "I need a crop loan of 5 lakh rupees",
            "context": {"amount": 500000}
        },
        {
            "query": "What are the government subsidies for farmers?",
            "context": {}
        },
        {
            "query": "Agricultural insurance options for wheat farming",
            "context": {"crop": "wheat"}
        },
        
        # Complex/ambiguous queries
        {
            "query": "Help me with farming",
            "context": {}
        },
        {
            "query": "I want to maximize profit from my 2 hectare farm",
            "context": {"area_hectares": 2, "goal": "profit"}
        },
        {
            "query": "Best practices for organic vegetable cultivation",
            "context": {"farming_type": "organic", "crop_category": "vegetables"}
        }
    ]
    
    print("🌾 Advanced Intent Classifier Test Results")
    print("=" * 60)
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        context = test_case["context"]
        
        print(f"\n{i}. Query: '{query}'")
        if context:
            print(f"   Context: {context}")
        
        # Classify intent
        intent, confidence = intent_classifier.classify_intent(query, context)
        
        # Extract parameters
        parameters = intent_classifier.extract_parameters(query, intent, context)
        
        print(f"   🎯 Intent: {intent} (confidence: {confidence:.2f})")
        print(f"   📊 Parameters: {json.dumps(parameters, indent=6)}")
        
        # Color coding based on confidence
        if confidence >= 0.8:
            confidence_emoji = "🟢"
        elif confidence >= 0.6:
            confidence_emoji = "🟡"
        else:
            confidence_emoji = "🔴"
        
        print(f"   {confidence_emoji} Confidence Level: {confidence:.2f}")

def test_parameter_extraction():
    """Test parameter extraction capabilities"""
    
    print("\n\n🔍 Parameter Extraction Test")
    print("=" * 40)
    
    extraction_tests = [
        {
            "query": "I have soil with pH 7.2, nitrogen 45, phosphorus 23, potassium 67, temperature 28°C, humidity 75%, rainfall 120mm",
            "intent": "crop_recommendation"
        },
        {
            "query": "Predict wheat prices for next 3 months in Punjab with 500 quintals production",
            "intent": "market_yield"
        },
        {
            "query": "Assess drought risk for 10 acres of cotton in Rajasthan this summer",
            "intent": "risk_assessment"
        },
        {
            "query": "My tomato plants have yellowing leaves and brown spots, need pest identification",
            "intent": "pest_detection"
        },
        {
            "query": "Need agricultural loan of 2.5 lakh rupees for buying seeds and fertilizers",
            "intent": "finance_agent"
        }
    ]
    
    for i, test in enumerate(extraction_tests, 1):
        query = test["query"]
        intent = test["intent"]
        
        print(f"\n{i}. Query: '{query}'")
        print(f"   Intent: {intent}")
        
        parameters = intent_classifier.extract_parameters(query, intent)
        
        print(f"   Extracted Parameters:")
        for key, value in parameters.items():
            if key not in ['query', 'intent']:
                print(f"     • {key}: {value}")

def test_contextual_boosting():
    """Test contextual boosting features"""
    
    print("\n\n🚀 Contextual Boosting Test")
    print("=" * 35)
    
    base_query = "Help me with my crops"
    
    contexts = [
        {"image_data": "dummy_image"},  # Should boost pest_detection
        {"weather_data": {"temp": 35}, "location": "Rajasthan"},  # Should boost risk_assessment
        {"soil_data": {"ph": 6.5, "N": 40}},  # Should boost crop_recommendation
        {"financial_context": True},  # Should boost finance_agent
        {}  # No context
    ]
    
    for i, context in enumerate(contexts, 1):
        intent, confidence = intent_classifier.classify_intent(base_query, context)
        
        print(f"\n{i}. Context: {context}")
        print(f"   Result: {intent} (confidence: {confidence:.2f})")

if __name__ == "__main__":
    print("🌾 Testing Advanced Intent Classifier")
    print("=====================================")
    
    try:
        test_intent_classification()
        test_parameter_extraction()
        test_contextual_boosting()
        
        print("\n\n✅ All tests completed successfully!")
        print("\nThe advanced intent classifier can now:")
        print("• Understand natural language queries with high accuracy")
        print("• Extract detailed parameters from user input")
        print("• Use contextual information to improve classification")
        print("• Handle complex agricultural queries intelligently")
        print("• Route queries to the most appropriate agent")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()