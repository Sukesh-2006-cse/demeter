from flask import Flask, request, jsonify
from flask_cors import CORS
from orchestrator.orchestrator import Orchestrator
import os
import logging
from werkzeug.utils import secure_filename
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# instantiate orchestrator (it will load agents)
BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(MODELS_DIR, exist_ok=True)

try:
    orch = Orchestrator(models_dir=MODELS_DIR)
    logger.info("Orchestrator initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize orchestrator: {e}")
    orch = None

@app.get("/health")
def health():
    """Health check endpoint with agent status"""
    if orch is None:
        return jsonify({"status": "error", "message": "Orchestrator not initialized"}), 500
    
    try:
        agent_status = orch.get_agent_status()
        return jsonify({
            "status": "ok", 
            "agents": list(orch.agents.keys()),
            "agent_status": agent_status,
            "total_agents": len(orch.agents)
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.post("/predict/<agent>")
def predict_agent(agent):
    """Direct agent prediction endpoint (legacy support)"""
    if orch is None:
        return jsonify({"ok": False, "error": "Orchestrator not initialized"}), 500
        
    payload = request.get_json(force=True, silent=True) or {}
    if agent not in orch.agents:
        return jsonify({
            "ok": False, 
            "error": "Unknown agent", 
            "available": list(orch.agents.keys())
        }), 400
    
    try:
        result = orch.agents[agent].predict(payload)
        return jsonify({"ok": True, "agent": agent, "result": result})
    except Exception as e:
        logger.error(f"Error in agent {agent}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post("/query")
def query():
    """
    Enhanced main entrypoint for natural text queries with advanced intent classification.
    
    Body: { 
        "text": "user query text",
        "context": { 
            "location": "optional location",
            "image_data": "optional base64 image",
            "user_preferences": {},
            "additional_data": {}
        }
    }
    """
    if orch is None:
        return jsonify({"ok": False, "error": "Orchestrator not initialized"}), 500
        
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "").strip()
    context = data.get("context", {})
    
    if not text:
        return jsonify({
            "ok": False, 
            "error": "No text provided",
            "example": {
                "text": "What crop should I plant?",
                "context": {"location": "Punjab", "soil_type": "clay"}
            }
        }), 400
    
    try:
        logger.info(f"Processing query: '{text}' with context keys: {list(context.keys())}")
        response = orch.handle_query(text, context)
        
        return jsonify({
            "ok": True,
            "query": text,
            **response
        })
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({
            "ok": False, 
            "error": str(e),
            "query": text
        }), 500

@app.post("/crop-recommendation")
def crop_recommendation():
    """Specific endpoint for crop recommendations"""
    if orch is None:
        return jsonify({"ok": False, "error": "Orchestrator not initialized"}), 500
        
    data = request.get_json(force=True, silent=True) or {}
    
    # Extract soil and climate parameters
    required_params = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    missing_params = [param for param in required_params if param not in data]
    
    if missing_params:
        return jsonify({
            "ok": False,
            "error": f"Missing required parameters: {missing_params}",
            "required": required_params
        }), 400
    
    # Create query text from parameters
    query_text = f"Recommend crops for soil with N={data['N']}, P={data['P']}, K={data['K']}, pH={data['ph']}, temperature={data['temperature']}°C, humidity={data['humidity']}%, rainfall={data['rainfall']}mm"
    
    context = {
        "soil_data": {k: data[k] for k in required_params},
        "location": data.get("location"),
        "area": data.get("area_hectares")
    }
    
    try:
        response = orch.handle_query(query_text, context)
        return jsonify({"ok": True, **response})
    except Exception as e:
        logger.error(f"Error in crop recommendation: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post("/market-prediction")
def market_prediction():
    """Specific endpoint for market price predictions"""
    if orch is None:
        return jsonify({"ok": False, "error": "Orchestrator not initialized"}), 500
        
    data = request.get_json(force=True, silent=True) or {}
    crop = data.get("crop")
    timeframe = data.get("timeframe", 30)
    
    if not crop:
        return jsonify({
            "ok": False,
            "error": "Crop name is required",
            "example": {"crop": "wheat", "timeframe": 30}
        }), 400
    
    query_text = f"Predict {crop} prices for the next {timeframe} days"
    context = {
        "crop": crop,
        "timeframe": timeframe,
        "location": data.get("location")
    }
    
    try:
        response = orch.handle_query(query_text, context)
        return jsonify({"ok": True, **response})
    except Exception as e:
        logger.error(f"Error in market prediction: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post("/risk-assessment")
def risk_assessment():
    """Specific endpoint for risk assessment"""
    if orch is None:
        return jsonify({"ok": False, "error": "Orchestrator not initialized"}), 500
        
    data = request.get_json(force=True, silent=True) or {}
    location = data.get("location")
    
    if not location:
        return jsonify({
            "ok": False,
            "error": "Location is required for risk assessment",
            "example": {"location": "Punjab", "crop": "wheat"}
        }), 400
    
    crop = data.get("crop", "crops")
    query_text = f"Assess weather and agricultural risks for {crop} in {location}"
    
    context = {
        "location": location,
        "crop": data.get("crop"),
        "weather_data": data.get("weather_data"),
        "time_period": data.get("time_period", "this season")
    }
    
    try:
        response = orch.handle_query(query_text, context)
        return jsonify({"ok": True, **response})
    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post("/pest-detection")
def pest_detection():
    """Specific endpoint for pest detection from images"""
    if orch is None:
        return jsonify({"ok": False, "error": "Orchestrator not initialized"}), 500
        
    data = request.get_json(force=True, silent=True) or {}
    image_data = data.get("image")
    
    if not image_data:
        return jsonify({
            "ok": False,
            "error": "Image data is required for pest detection",
            "example": {"image": "base64_encoded_image_data", "crop_type": "wheat"}
        }), 400
    
    query_text = "Identify pest or disease in this image"
    context = {
        "image_data": image_data,
        "crop_type": data.get("crop_type"),
        "symptoms": data.get("symptoms", [])
    }
    
    try:
        response = orch.handle_query(query_text, context)
        return jsonify({"ok": True, **response})
    except Exception as e:
        logger.error(f"Error in pest detection: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post("/upload-image")
def upload_image():
    """Upload image for pest detection"""
    if 'image' not in request.files:
        return jsonify({"ok": False, "error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"ok": False, "error": "No file selected"}), 400
    
    try:
        # Read and encode image
        image_data = file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        return jsonify({
            "ok": True,
            "image_data": image_base64,
            "filename": secure_filename(file.filename),
            "size": len(image_data)
        })
        
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get("/languages")
def get_languages():
    """Get supported languages"""
    try:
        from utils.translation import translation_service
        languages = translation_service.get_supported_languages()
        return jsonify({"ok": True, "languages": languages})
    except Exception as e:
        logger.error(f"Error getting languages: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get("/agent-status")
def agent_status():
    """Get detailed status of all agents"""
    if orch is None:
        return jsonify({"ok": False, "error": "Orchestrator not initialized"}), 500
    
    try:
        status = orch.get_agent_status()
        return jsonify({"ok": True, "agent_status": status})
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post("/clear-cache")
def clear_cache():
    """Clear orchestrator cache"""
    if orch is None:
        return jsonify({"ok": False, "error": "Orchestrator not initialized"}), 500
    
    try:
        orch.clear_cache()
        return jsonify({"ok": True, "message": "Cache cleared successfully"})
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "ok": False,
        "error": "Endpoint not found",
        "available_endpoints": [
            "/health", "/query", "/crop-recommendation", 
            "/market-prediction", "/risk-assessment", "/pest-detection"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "ok": False,
        "error": "Internal server error",
        "message": "Please check the server logs for more details"
    }), 500

if __name__ == "__main__":
    print("Starting Demeter backend...")
    app.run(host="0.0.0.0", port=5000, debug=True)
