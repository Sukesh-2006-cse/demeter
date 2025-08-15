import os, joblib, numpy as np
from .base_agent import BaseAgent

class MarketYieldAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("MarketYield", models_dir=models_dir)
        p1 = os.path.join(self.models_dir, "market_price.pkl")
        p2 = os.path.join(self.models_dir, "yield_model.pkl")
        self.price_model = joblib.load(p1) if os.path.exists(p1) else None
        self.yield_model = joblib.load(p2) if os.path.exists(p2) else None

    def predict(self, payload: dict) -> dict:
        ctx = payload.get("context", {})
        crop_idx = int(ctx.get("crop_idx", 0))  # mapping must be agreed with frontend
        month = int(ctx.get("month", 7))
        region = int(ctx.get("region", 0))
        area = float(ctx.get("area", 1.0))
        if self.price_model:
            Xp = np.array([[crop_idx, month, region, 0.0, 0.0]])
            price = float(self.price_model.predict(Xp)[0])
        else:
            price = 18.0
        if self.yield_model:
            Xy = np.array([[crop_idx, area, float(ctx.get("ph",6.5)), float(ctx.get("N",150)), float(ctx.get("P",50)), float(ctx.get("K",100)), float(ctx.get("rain",120)), float(ctx.get("temp",25)), month]])
            yld = float(self.yield_model.predict(Xy)[0])
        else:
            yld = 3.0
        revenue = price * yld * (area)  # price per kg * yield (t/ha) mismatch units in prototype — keep consistent when integrating real data
        # simple cost
        cost = float(ctx.get("cost", 8000.0))
        profit = revenue - cost
        return {"predicted_price": round(price,2), "estimated_yield": round(yld,3), "estimated_profit": round(profit,2)}

    def format_result_text(self, result, context):
        return f"Expected yield {result['estimated_yield']} q/ha, price ₹{result['predicted_price']}/kg, estimated profit ₹{result['estimated_profit']}."
