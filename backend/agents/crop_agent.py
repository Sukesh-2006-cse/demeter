import os, joblib, numpy as np
from .base_agent import BaseAgent

class CropAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("CropAdvisory", models_dir=models_dir)
        path = os.path.join(self.models_dir, "crop_recommendation.pkl")
        self.model = joblib.load(path) if os.path.exists(path) else None

    def predict(self, payload: dict) -> dict:
        # expected payload: {"text": "...", "context": {"ph":..., "N":..., "P":..., "K":..., "rain":..., "temp":..., "season":...}}
        ctx = payload.get("context", {})
        # parse features with defaults
        ph = float(ctx.get("ph", 6.5))
        N = float(ctx.get("N", 150))
        P = float(ctx.get("P", 50))
        K = float(ctx.get("K", 100))
        rain = float(ctx.get("rain", 120))
        temp = float(ctx.get("temp", 25))
        season = int(ctx.get("season", 0))
        X = np.array([[ph, N, P, K, rain, temp, season]])
        if self.model:
            pred = self.model.predict(X)[0]
            probs = None
            try:
                probs = self.model.predict_proba(X)[0].tolist()
            except Exception:
                probs = None
            return {"top_crop": pred, "confidence": probs}
        # fallback heuristic
        if rain > 150 and 5.0 <= ph <= 6.8:
            return {"top_crop": "rice", "confidence": 0.6}
        if temp < 18:
            return {"top_crop": "wheat", "confidence": 0.55}
        return {"top_crop": "maize", "confidence": 0.5}

    def format_result_text(self, result, context):
        crop = result.get("top_crop")
        conf = result.get("confidence")
        return f"Recommended crop: {crop}. Confidence: {round(conf[0],3) if isinstance(conf, list) and len(conf)>0 else (round(conf,2) if isinstance(conf, float) else 'N/A')}."
