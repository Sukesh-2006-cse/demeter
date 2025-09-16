import os, joblib
from abc import ABC, abstractmethod

def load_agent_classes(models_dir):
    """
    Instantiate agent classes and return dict keyed by intent names:
      crop, market_yield, risk, finance, pest
    """
    from .crop_agent import CropAgent
    from .market_yield_agent import MarketYieldAgent
    from .risk_agent import RiskAgent
    from .finance_agent import FinanceAgent
    from .pest_agent import PestAgent

    agents = {
        "crop": CropAgent(models_dir=models_dir),
        "market_yield": MarketYieldAgent(models_dir=models_dir),
        "risk": RiskAgent(models_dir=models_dir),
        "finance": FinanceAgent(models_dir=models_dir),
        "pest": PestAgent(models_dir=models_dir)
    }
    return agents

class BaseAgent(ABC):
    def __init__(self, name, models_dir=None):
        self.name = name
        self.models_dir = models_dir

    @abstractmethod
    def predict(self, payload: dict) -> dict:
        pass

    def format_result_text(self, result: dict, context: dict) -> str:
        # default simple conversion
        return str(result)
