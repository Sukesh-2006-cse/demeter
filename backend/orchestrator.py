from services.translator import MultilingualTranslator
from services.intent_classifier import IntentClassifier
import logging

class Orchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.translator = MultilingualTranslator()
        self.intent_classifier = IntentClassifier()
        
    def route(self, query):
        """Main routing logic for processing user queries"""
        try:
            # Process multilingual input
            query_en, source_lang = self.translator.process_multilingual(query)
            
            # Classify intent
            intent = self.intent_classifier.predict_intent(query_en)
            
            # Route to appropriate agent
            agent = self._select_agent(intent, query_en)
            
            # Get prediction from the chosen agent
            response_en = agent.predict(query_en)
            
            # Translate back to original language if needed
            if source_lang != 'en':
                response_translated = self.translator.translate_from_english(response_en, source_lang)
                return response_translated
            else:
                return response_en
                
        except Exception as e:
            logging.error(f"Orchestrator error: {e}")
            return "I apologize, but I encountered an error processing your request. Please try again or rephrase your question."
    
    def _select_agent(self, intent, query):
        """Select the most appropriate agent based on intent and query content"""
        query_lower = query.lower()
        
        # Legal-related queries
        if intent == 'legal' or any(word in query_lower for word in 
            ['legal', 'law', 'compliance', 'regulation', 'license', 'permit', 'contract']):
            return self.agents.get('legal', self.agents.get('general'))
            
        # Compliance-related queries  
        elif intent == 'compliance' or any(word in query_lower for word in 
            ['gst', 'roc', 'filing', 'return', 'audit', 'penalty']):
            return self.agents.get('compliance', self.agents.get('general'))
            
        # Business-related queries
        elif intent == 'business' or any(word in query_lower for word in 
            ['startup', 'business plan', 'market', 'strategy', 'operations']):
            return self.agents.get('business', self.agents.get('general'))
            
        # Finance-related queries
        elif intent == 'finance' or any(word in query_lower for word in 
            ['loan', 'funding', 'investment', 'scheme', 'bank', 'insurance']):
            return self.agents.get('finance', self.agents.get('general'))
            
        # Advisory queries
        elif intent == 'advisory':
            return self.agents.get('business', self.agents.get('general'))
            
        # Default to general agent
        else:
            return self.agents.get('general', self.agents.get('legal'))
    
    def get_agent_info(self):
        """Return information about available agents"""
        agent_info = {
            'legal': 'Legal advice for business registration, licensing, compliance, contracts, and regulations',
            'compliance': 'Compliance guidance for GST, ROC, labor laws, environmental, and audit requirements', 
            'business': 'Business advisory for startups, strategy, operations, growth, and planning',
            'finance': 'Financial guidance for loans, schemes, investment, banking, and tax planning'
        }
        return agent_info
