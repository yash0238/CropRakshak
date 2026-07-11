"""
Diagnosis API Routes
Handles crop image diagnosis requests
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import json

from agents import ImageDiagnosisAgent
from agents import AnalyticsAgent

router = APIRouter()

# Initialize agents
diagnosis_agent = ImageDiagnosisAgent()
analytics_agent = AnalyticsAgent()

@router.post("/analyze")
async def analyze_crop_image(
    image: UploadFile = File(...),
    crop_type: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    weather: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None)
):
    """
    Analyze uploaded crop image for disease detection
    
    Parameters:
    - image: Crop/leaf image file
    - crop_type: Type of crop (optional)
    - location: JSON string with location data (optional)
    - weather: JSON string with weather data (optional)
    - user_id: User ID for analytics (optional)
    """
    
    try:
        # Validate image
        if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid image format. Only JPEG/PNG allowed."
            )
        
        # Read image data
        image_data = await image.read()
        
        if len(image_data) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(
                status_code=400,
                detail="Image size too large. Maximum 10MB allowed."
            )
        
        # Parse optional JSON parameters
        location_data = json.loads(location) if location else None
        weather_data = json.loads(weather) if weather else None
        
        # Analyze image
        result = await diagnosis_agent.analyze_crop_image(
            image_data=image_data,
            crop_type=crop_type,
            location=location_data,
            weather=weather_data
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Log to analytics (async, non-blocking)
        if user_id:
            await analytics_agent.log_diagnosis_event({
                "userId": user_id,
                "disease": result["data"].get("disease"),
                "confidence": result["data"].get("confidence"),
                "severity": result["data"].get("severity"),
                "cropType": crop_type,
                "location": location_data
            })
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/disease-info/{disease_name}")
async def get_disease_info(disease_name: str, language: str = "en"):
    """Get detailed information about a specific disease"""
    
    try:
        result = await diagnosis_agent.get_disease_info(disease_name, language)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "diagnosis"}
