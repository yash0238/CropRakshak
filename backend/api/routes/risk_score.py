"""
Risk Score API Routes
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from agents import RiskPredictionAgent, AnalyticsAgent

router = APIRouter()
risk_agent = RiskPredictionAgent()
analytics_agent = AnalyticsAgent()

class RiskScoreRequest(BaseModel):
    userId: Optional[str] = None
    weatherData: Dict[str, Any]
    diseaseHistory: List[Dict[str, Any]] = []
    cropInfo: Dict[str, Any]
    location: Dict[str, Any]

@router.post("/calculate")
async def calculate_risk_score(request: RiskScoreRequest):
    """Calculate farm risk score"""
    
    try:
        result = await risk_agent.calculate_farm_risk_score(
            weather_data=request.weatherData,
            disease_history=request.diseaseHistory,
            crop_info=request.cropInfo,
            location=request.location
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Log to analytics
        if request.userId:
            await analytics_agent.log_risk_score_event({
                "userId": request.userId,
                "overallScore": result["data"]["overallScore"],
                "riskLevel": result["data"]["riskLevel"],
                "weatherRisk": result["data"]["components"]["weatherRisk"],
                "diseaseRisk": result["data"]["components"]["diseaseRisk"],
                "cropHealthRisk": result["data"]["components"]["cropHealthRisk"],
                "location": request.location
            })
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "risk-score"}
