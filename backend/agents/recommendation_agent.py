"""
Recommendation Agent
Generates actionable farming decisions based on all available data
"""

import google.generativeai as genai
from typing import Dict, Any, Optional
from config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

class RecommendationAgent:
    """Agent for generating farmer-friendly recommendations"""
    
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL_PRO)
    
    async def get_decision_card(
        self,
        question: str,
        context: Dict[str, Any],
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate decision card for specific farmer questions
        
        Examples:
        - "Should I spray pesticide today?"
        - "Should I irrigate today?"
        - "What fertilizer should I use?"
        """
        
        language_map = {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi",
            "ta": "Tamil",
            "te": "Telugu"
        }
        
        prompt = f"""You are an agricultural advisor helping a farmer make a decision.

Farmer's Question: {question}

Context:
- Weather: {context.get('weather', {})}
- Crop: {context.get('crop', 'Not specified')}
- Recent Diseases: {context.get('diseases', 'None')}
- Farm Risk Score: {context.get('riskScore', 'Unknown')}
- Location: {context.get('location', 'Not specified')}

Provide a clear, actionable decision card. Respond in {language_map.get(language, 'English')}.

Format:
1. Decision: YES/NO/WAIT (clear answer)
2. Reasoning: Why this decision (2-3 points)
3. Timing: When to act (if applicable)
4. Additional Tips: 1-2 practical tips
5. Risks: What to watch out for

Keep it simple and farmer-friendly. Use emojis for visual clarity."""
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "data": {
                    "question": question,
                    "recommendation": response.text,
                    "language": language,
                    "timestamp": context.get("timestamp")
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_comprehensive_recommendations(
        self,
        farm_data: Dict[str, Any],
        language: str = "en"
    ) -> Dict[str, Any]:
        """Generate comprehensive farming recommendations"""
        
        prompt = f"""As an agricultural expert, provide comprehensive farming recommendations.

Farm Details:
- Crop: {farm_data.get('crop', 'Not specified')}
- Farm Size: {farm_data.get('farmSize', 'Unknown')} acres
- Location: {farm_data.get('location', {})}
- Current Risk Score: {farm_data.get('riskScore', 'Unknown')}/100
- Weather: {farm_data.get('weather', {})}
- Recent Issues: {farm_data.get('recentIssues', 'None')}

Provide recommendations for:
1. Immediate Actions (Today/Tomorrow)
2. This Week
3. This Month
4. This Season
5. Next Season Planning

Format as actionable bullet points. Include organic and chemical options where applicable."""
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "data": {
                    "recommendations": response.text,
                    "language": language
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
