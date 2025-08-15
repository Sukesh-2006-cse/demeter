# lightweight intent classifier using keyword heuristics + fallback
class IntentClassifier:
    def __init__(self):
        # simple keyword map
        self.map = {
            "crop": ["crop","plant","sow","fertilizer","which crop","what crop","suitability"],
            "market_yield": ["price","market","sell","yield","profit","income","market price"],
            "risk": ["pest","disease","water","irrigation","risk","outbreak","attack"],
            "finance": ["loan","insurance","subsidy","scheme","pmkisan","pm-kisan","credit","loan eligibility"]
        }

    def predict_intent(self, text_en: str):
        t = text_en.lower()
        scores = {k: 0 for k in self.map.keys()}
        for k, kw_list in self.map.items():
            for kw in kw_list:
                if kw in t:
                    scores[k] += 1
        # pick highest score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, top_score = sorted_scores[0]
        if top_score == 0:
            return "crop"  # default to crop advisory
        return top_intent
