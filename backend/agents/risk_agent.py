import os, joblib, numpy as np
from .base_agent import BaseAgent

class RiskAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("RiskAgent", models_dir=models_dir)
        p_pest = os.path.join(self.models_dir, "pest_risk.pkl")
        p_yield_risk = os.path.join(self.models_dir, "yield_risk.pkl")
        self.pest_model = joblib.load(p_pest) if os.path.exists(p_pest) else None
        self.yield_risk_model = joblib.load(p_yield_risk) if os.path.exists(p_yield_risk) else None

    def predict(self, payload: dict) -> dict:
        ctx = payload.get("context", {})
        temp = float(ctx.get("temp", 27))
        hum = float(ctx.get("hum", 70))
        recent_rain = float(ctx.get("recent_rain", 10))
        crop_idx = int(ctx.get("crop_idx", 0))
        if self.pest_model:
            Xp = np.array([[temp, hum, recent_rain, crop_idx, int(ctx.get("month",7))]])
            pest_prob = float(self.pest_model.predict_proba(Xp)[0][1])
        else:
            pest_prob = min(0.95, max(0.05, (hum-50)/100 + (temp-20)/100))
        # yield risk
        if self.yield_risk_model:
            Xr = np.array([[int(ctx.get("crop_idx",0)), float(ctx.get("area",1.0)), float(ctx.get("ph",6.5)), float(ctx.get("N",150)), float(ctx.get("P",50)), float(ctx.get("K",100)), float(ctx.get("rain",120)), float(ctx.get("temp",25)), int(ctx.get("month",7))]])
            risk = int(self.yield_risk_model.predict(Xr)[0])
        else:
            risk = 0
        advice = "Monitor closely for fungal diseases" if pest_prob > 0.6 else "Low pest risk in next week"
        return {"pest_probability": round(pest_prob,3), "yield_risk": bool(risk), "advice": advice}

    def format_result_text(self, result, context):
        return f"Pest outbreak probability {result['pest_probability']*100:.1f}%. {result['advice']}"
