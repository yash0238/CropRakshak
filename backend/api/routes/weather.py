"""
Weather API Routes
Handles weather intelligence requests
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional

from agents import WeatherIntelligenceAgent

router = APIRouter()

# Initialize agent
weather_agent = WeatherIntelligenceAgent()

@router.get("/current")
async def get_current_weather(
    latitude: float = Query(..., description="Location latitude"),
    longitude: float = Query(..., description="Location longitude"),
    forecast_days: int = Query(7, ge=1, le=14, description="Number of forecast days")
):
    """
    Get current weather and forecast with disease risk analysis
    
    Parameters:
    - latitude: Location latitude
    - longitude: Location longitude
    - forecast_days: Number of days to forecast (1-14, default 7)
    """
    
    try:
        result = await weather_agent.get_weather_data(
            latitude=latitude,
            longitude=longitude,
            forecast_days=forecast_days
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/irrigation-recommendation")
async def get_irrigation_recommendation(
    latitude: float = Query(..., description="Location latitude"),
    longitude: float = Query(..., description="Location longitude"),
    crop_type: str = Query(..., description="Type of crop"),
    soil_type: Optional[str] = Query(None, description="Type of soil")
):
    """
    Get irrigation recommendations based on weather forecast
    
    Parameters:
    - latitude: Location latitude
    - longitude: Location longitude
    - crop_type: Type of crop
    - soil_type: Type of soil (optional)
    """
    
    try:
        result = await weather_agent.get_irrigation_recommendation(
            latitude=latitude,
            longitude=longitude,
            crop_type=crop_type,
            soil_type=soil_type
        )
        
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
    return {"status": "healthy", "service": "weather"}
