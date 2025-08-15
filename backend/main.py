from flask import Flask, request, jsonify
from flask_cors import CORS
from orchestrator.orchestrator import Orchestrator
import os

app = Flask(__name__)
CORS(app)

# instantiate orchestrator (it will load agents)
BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(MODELS_DIR, exist_ok=True)

orch = Orchestrator(models_dir=MODELS_DIR)

@app.get("/health")
def health():
    return jsonify({"status":"ok", "agents": list(orch.agents.keys())})

@app.post("/predict/<agent>")
def predict_agent(agent):
    payload = request.get_json(force=True, silent=True) or {}
    if agent not in orch.agents:
        return jsonify({"ok": False, "error": "Unknown agent", "available": list(orch.agents.keys())}), 400
    try:
        result = orch.agents[agent].predict(payload)
        return jsonify({"ok": True, "agent": agent, "result": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post("/query")
def query():
    """
    Main entrypoint for natural text queries.
    Body: { "text": "...", "context": { optional structured data } }
    """
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")
    context = data.get("context", {})
    if not text:
        return jsonify({"ok": False, "error": "No text provided"}), 400
    try:
        response = orch.handle_query(text, context)
        return jsonify({"ok": True, **response})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Demeter backend...")
    app.run(host="0.0.0.0", port=5000, debug=True)
