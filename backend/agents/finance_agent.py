from .base_agent import BaseAgent

class FinanceAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("FinanceAgent", models_dir=models_dir)
        # rules loaded from file or hardcoded
        self.schemes = [
            {"name":"PM-KISAN", "min_acre":0},
            {"name":"PMFBY Insurance", "min_acre":0.1},
            {"name":"Drip Subsidy", "min_acre":0.5}
        ]

    def predict(self, payload):
        ctx = payload.get("context", {})
        land = float(ctx.get("area", 1.0))
        eligible = [s["name"] for s in self.schemes if land >= s["min_acre"]]
        tip = f"Farmers in {ctx.get('region','your area')} often delay irrigation to reduce water use."
        return {"eligible_schemes": eligible, "tip": tip}

    def format_result_text(self, result, context):
        return f"Eligible schemes: {', '.join(result['eligible_schemes'])}. Tip: {result['tip']}"
