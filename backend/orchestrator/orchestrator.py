import os, json
from langdetect import detect, LangDetectException
from googletrans import Translator
from .intent_classifier import IntentClassifier
from ..agents.base_agent import load_agent_classes

class Orchestrator:
    def __init__(self, models_dir: str):
        self.models_dir = models_dir
        self.translator = Translator()
        self.intent_clf = IntentClassifier()
        # load agents (factory)
        self.agents = load_agent_classes(models_dir)
        # path for simple cache (daily sync)
        self.cache_file = os.path.join(models_dir, "daily_cache.json")
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, "w") as f:
                json.dump({}, f)

    def detect_language(self, text: str):
        try:
            lang = detect(text)
        except LangDetectException:
            lang = "en"
        return lang

    def to_en(self, text: str, src=None):
        try:
            if src is None:
                src = self.detect_language(text)
            if src == "en":
                return text
            return self.translator.translate(text, src=src, dest="en").text
        except Exception:
            return text

    def from_en(self, text_en: str, dest_lang="en"):
        try:
            if dest_lang == "en":
                return text_en
            return self.translator.translate(text_en, src="en", dest=dest_lang).text
        except Exception:
            return text_en

    def handle_query(self, text: str, context: dict):
        # 1) detect language and translate to EN
        lang = self.detect_language(text)
        text_en = self.to_en(text, src=lang)

        # 2) classify intent
        intent = self.intent_clf.predict_intent(text_en)

        # 3) prepare structured input: merge context & parse basic slots
        payload = {"text": text_en, "context": context}
        # quick slot parser for numbers / crop words could be added here

        # 4) route to agent(s)
        if intent in self.agents:
            agent = self.agents[intent]
            result = agent.predict(payload)
            # 5) generate NLG template
            answer_en = agent.format_result_text(result, context)
        else:
            # fallback: try to answer using crop agent if keywords match
            agent = self.agents.get("crop")
            result = {"message": "I could not classify intent. Please ask about crop, market, risk or finance."}
            answer_en = result.get("message")

        # 6) translate back
        answer_local = self.from_en(answer_en, dest_lang=lang)

        response = {
            "language": lang,
            "intent": intent,
            "source_agent": agent.name if agent else None,
            "result": result,
            "answer": answer_local
        }
        return response

    # simple daily cache utilities
    def update_cache(self, key, value):
        with open(self.cache_file, "r+") as f:
            data = json.load(f)
            data[key] = value
            f.seek(0)
            json.dump(data, f)
            f.truncate()

    def read_cache(self, key):
        with open(self.cache_file, "r") as f:
            data = json.load(f)
        return data.get(key)
