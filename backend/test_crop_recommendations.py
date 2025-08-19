from agents.crop_agent import CropAgent

def test_crop_recommendations():
    # Create an instance of the CropAgent
    agent = CropAgent()
    
    # Test with sample soil and climate data
    result = agent.predict({
        'context': {
            'N': 90,
            'P': 42,
            'K': 43,
            'temperature': 20,
            'humidity': 82,
            'ph': 6.5,
            'rainfall': 200
        }
    })
    
    # Print the results
    print('Top crop:', result['top_crop'])
    print('\nRecommended crops:', result['recommended_crops'])
    print('\nDetailed recommendations:')
    for i, crop in enumerate(result['detailed_recommendations']):
        print(f'{i+1}. {crop["crop"]} (Confidence: {crop["confidence"]:.1%})')
    
    # Print the formatted result text
    print('\nFormatted result text:')
    print(agent.format_result_text(result, {}))

if __name__ == '__main__':
    test_crop_recommendations()