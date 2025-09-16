import os, joblib, numpy as np
from .base_agent import BaseAgent

class MarketYieldAgent(BaseAgent):
    def __init__(self, models_dir=None):
        super().__init__("market_yield", models_dir=models_dir)
        
        # Try to load models from multiple locations
        model_paths = [
            (os.path.join("models", "market_model.pkl"), "market"),
            (os.path.join("models", "yield_model.pkl"), "yield"),
            (os.path.join(models_dir or "", "market_model.pkl"), "market"),
            (os.path.join(models_dir or "", "yield_model.pkl"), "yield"),
        ]
        
        self.price_model = None
        self.yield_model = None
        
        for path, model_type in model_paths:
            if os.path.exists(path):
                try:
                    model = joblib.load(path)
                    if model_type == "market":
                        self.price_model = model
                        print(f"Loaded market price model from {path}")
                    elif model_type == "yield":
                        self.yield_model = model
                        print(f"Loaded yield model from {path}")
                except Exception as e:
                    print(f"Failed to load {model_type} model from {path}: {e}")

    def predict(self, payload: dict) -> dict:
        """Main prediction method for market price and yield prediction"""
        context = payload.get("context", {})
        text = payload.get("text", "")
        
        try:
            # Extract parameters from context
            crop = context.get("crop", "wheat").lower()
            location = context.get("location", "unknown")
            timeframe = int(context.get("timeframe", 30))
            area_hectares = float(context.get("area_hectares", context.get("area", 1.0)))
            
            # Soil conditions for yield prediction
            soil_conditions = context.get("soil_conditions", {})
            N = float(soil_conditions.get("N", context.get("N", 50)))
            P = float(soil_conditions.get("P", context.get("P", 30)))
            K = float(soil_conditions.get("K", context.get("K", 40)))
            ph = float(soil_conditions.get("ph", context.get("ph", 6.5)))
            
            # Weather conditions for yield prediction
            weather_conditions = context.get("weather_conditions", {})
            temperature = float(weather_conditions.get("temperature", context.get("temperature", 25)))
            humidity = float(weather_conditions.get("humidity", context.get("humidity", 60)))
            rainfall = float(weather_conditions.get("rainfall", context.get("rainfall", 100)))
            
            # Predict market price
            if self.price_model:
                # Features: historical_price, demand, supply, season, weather_score
                crop_idx = self._get_crop_index(crop)
                season = self._get_season_index()
                weather_score = self._calculate_weather_score(temperature, humidity, rainfall)
                
                price_features = np.array([[crop_idx, 0.8, 0.7, season, weather_score]])
                predicted_price = float(self.price_model.predict(price_features)[0])
            else:
                predicted_price = self._get_fallback_price(crop)
            
            # Predict yield
            if self.yield_model:
                # Features: N, P, K, temperature, humidity, ph, rainfall, area
                yield_features = np.array([[N, P, K, temperature, humidity, ph, rainfall, area_hectares]])
                predicted_yield = float(self.yield_model.predict(yield_features)[0])
            else:
                predicted_yield = self._get_fallback_yield(crop, area_hectares)
            
            # Calculate financial projections
            total_yield = predicted_yield * area_hectares
            total_revenue = total_yield * predicted_price
            estimated_cost = self._estimate_costs(crop, area_hectares)
            estimated_profit = total_revenue - estimated_cost
            
            return {
                "success": True,
                "crop": crop,
                "location": location,
                "timeframe_days": timeframe,
                "area_hectares": area_hectares,
                "predicted_price_per_kg": round(predicted_price, 2),
                "predicted_yield_tons_per_hectare": round(predicted_yield, 2),
                "total_expected_yield_tons": round(total_yield, 2),
                "total_expected_revenue": round(total_revenue, 2),
                "estimated_costs": round(estimated_cost, 2),
                "estimated_profit": round(estimated_profit, 2),
                "confidence_price": 0.75,
                "confidence_yield": 0.8,
                "message": f"For {crop} cultivation over {area_hectares} hectares: Expected yield is {predicted_yield:.1f} tons/hectare, market price ₹{predicted_price:.2f}/kg, potential profit ₹{estimated_profit:,.2f}",
                "agent_used": "market_yield"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Market/yield prediction failed: {str(e)}",
                "agent_used": "market_yield"
            }

    def _get_crop_index(self, crop):
        """Convert crop name to index for model"""
        crop_mapping = {
            "wheat": 0, "rice": 1, "corn": 2, "barley": 3, "cotton": 4,
            "sugarcane": 5, "soybean": 6, "potato": 7, "tomato": 8, "onion": 9
        }
        return crop_mapping.get(crop.lower(), 0)

    def _get_season_index(self):
        """Get current season index"""
        import datetime
        month = datetime.datetime.now().month
        if month in [12, 1, 2]:  # Winter
            return 0
        elif month in [3, 4, 5]:  # Spring
            return 1
        elif month in [6, 7, 8]:  # Summer
            return 2
        else:  # Fall
            return 3

    def _calculate_weather_score(self, temp, humidity, rainfall):
        """Calculate weather suitability score (0-1)"""
        # Ideal conditions: temp 20-30, humidity 40-70, rainfall 50-150
        temp_score = 1.0 - abs(temp - 25) / 25
        humidity_score = 1.0 - abs(humidity - 55) / 55
        rainfall_score = 1.0 - abs(rainfall - 100) / 100
        
        return max(0, min(1, (temp_score + humidity_score + rainfall_score) / 3))

    def _get_fallback_price(self, crop):
        """Fallback price estimates when model is not available"""
        fallback_prices = {
            "wheat": 25.0, "rice": 30.0, "corn": 20.0, "barley": 22.0,
            "cotton": 45.0, "sugarcane": 3.5, "soybean": 40.0,
            "potato": 15.0, "tomato": 25.0, "onion": 18.0
        }
        return fallback_prices.get(crop.lower(), 25.0)

    def _get_fallback_yield(self, crop, area):
        """Fallback yield estimates when model is not available"""
        fallback_yields = {
            "wheat": 3.5, "rice": 4.2, "corn": 5.8, "barley": 3.0,
            "cotton": 1.8, "sugarcane": 70.0, "soybean": 2.5,
            "potato": 25.0, "tomato": 40.0, "onion": 20.0
        }
        return fallback_yields.get(crop.lower(), 3.5)

    def _estimate_costs(self, crop, area):
        """Estimate cultivation costs"""
        cost_per_hectare = {
            "wheat": 25000, "rice": 30000, "corn": 28000, "barley": 22000,
            "cotton": 35000, "sugarcane": 45000, "soybean": 25000,
            "potato": 40000, "tomato": 50000, "onion": 35000
        }
        base_cost = cost_per_hectare.get(crop.lower(), 25000)
        return base_cost * area

    def process_query(self, text: str, payload: dict) -> dict:
        """Process query using the predict method"""
        return self.predict(payload)

    def format_result_text(self, result, context):
        """Format result into readable text"""
        if not result.get("success"):
            return f"Unable to predict market/yield data: {result.get('error', 'Unknown error')}"
        
        crop = result.get("crop", "crop")
        yield_per_ha = result.get("predicted_yield_tons_per_hectare", 0)
        price = result.get("predicted_price_per_kg", 0)
        profit = result.get("estimated_profit", 0)
        
        return f"For {crop}: Expected yield {yield_per_ha} tons/hectare, price ₹{price}/kg, estimated profit ₹{profit:,.0f}"
