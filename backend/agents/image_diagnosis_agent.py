"""
Image Diagnosis Agent
Uses Gemini Vision to analyze crop images and detect diseases
"""

import google.generativeai as genai
from PIL import Image
import io
import base64
from typing import Dict, Any, Optional
from config import settings

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

class ImageDiagnosisAgent:
    """Agent for crop disease diagnosis using Gemini Vision"""
    
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL_VISION)
        self.generation_config = {
            "temperature": 0.4,  # Lower for more precise diagnosis
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
    
    async def analyze_crop_image(
        self,
        image_data: bytes,
        crop_type: Optional[str] = None,
        location: Optional[Dict] = None,
        weather: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analyze crop image for disease detection
        
        Args:
            image_data: Image bytes
            crop_type: Type of crop (optional)
            location: Location details (optional)
            weather: Weather context (optional)
            
        Returns:
            Dict with disease, confidence, severity, description, treatment
        """
        
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Construct context-aware prompt
            prompt = self._build_diagnosis_prompt(crop_type, location, weather)
            
            # Generate response
            response = self.model.generate_content(
                [prompt, image],
                generation_config=self.generation_config
            )
            
            # Parse structured response
            diagnosis = self._parse_diagnosis_response(response.text)
            
            return {
                "success": True,
                "data": diagnosis
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_diagnosis_prompt(
        self,
        crop_type: Optional[str],
        location: Optional[Dict],
        weather: Optional[Dict]
    ) -> str:
        """Build context-aware diagnosis prompt"""
        
        context = []
        
        if crop_type:
            context.append(f"Crop Type: {crop_type}")
        
        if location:
            context.append(f"Location: {location.get('district', '')}, {location.get('state', '')}")
        
        if weather:
            context.append(f"Weather: {weather.get('temperature', '')}°C, Humidity: {weather.get('humidity', '')}%")
        
        context_str = "\n".join(context) if context else "No additional context provided"
        
        prompt = f"""You are an expert agricultural pathologist. Analyze this crop image and provide a detailed diagnosis.

{context_str}

Please provide your analysis in the following JSON format:
{{
    "disease": "Name of disease or 'Healthy' if no disease detected",
    "confidence": 0.0 to 1.0,
    "severity": "none/low/medium/high/critical",
    "description": "Brief description of the condition",
    "symptoms": ["symptom1", "symptom2", ...],
    "causes": ["cause1", "cause2", ...],
    "treatment": {{
        "immediate": ["action1", "action2", ...],
        "preventive": ["action1", "action2", ...],
        "organic": ["solution1", "solution2", ...],
        "chemical": ["pesticide1", "pesticide2", ...]
    }},
    "affectedParts": ["leaf", "stem", "fruit", etc.],
    "spreadRisk": "low/medium/high",
    "economicImpact": "Brief description of potential losses"
}}

Be precise, practical, and farmer-friendly. Focus on actionable advice."""
        
        return prompt
    
    def _parse_diagnosis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured diagnosis"""
        
        import json
        import re
        
        try:
            # Extract JSON from response (handles markdown code blocks)
            json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response_text
            
            diagnosis = json.loads(json_str)
            return diagnosis
            
        except json.JSONDecodeError:
            # Fallback parsing if JSON extraction fails
            return {
                "disease": "Unknown",
                "confidence": 0.0,
                "severity": "unknown",
                "description": response_text,
                "symptoms": [],
                "treatment": {
                    "immediate": [],
                    "preventive": [],
                    "organic": [],
                    "chemical": []
                }
            }
    
    async def get_disease_info(self, disease_name: str, language: str = "en") -> Dict[str, Any]:
        """Get detailed information about a specific disease"""
        
        language_map = {
            "en": "English",
            "hi": "Hindi (हिंदी)",
            "mr": "Marathi (मराठी)",
            "ta": "Tamil (தமிழ்)",
            "te": "Telugu (తెలుగు)"
        }
        
        prompt = f"""Provide detailed information about the crop disease: {disease_name}

Respond in {language_map.get(language, 'English')}.

Include:
1. What is this disease?
2. How to identify it?
3. What causes it?
4. How does it spread?
5. Treatment methods (organic and chemical)
6. Prevention strategies
7. Economic impact

Keep explanations simple and farmer-friendly."""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "success": True,
                "info": response.text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
