"""
Government Schemes API Routes
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any

from agents import GovernmentSchemeAgent

router = APIRouter()
scheme_agent = GovernmentSchemeAgent()

class FarmerProfileRequest(BaseModel):
    farmSize: float
    crops: list[str]
    state: str
    landOwnership: str = "Owner"
    language: str = "en"

@router.post("/find-eligible")
async def find_eligible_schemes(request: FarmerProfileRequest):
    """Find government schemes based on farmer profile"""
    
    try:
        result = await scheme_agent.find_eligible_schemes(
            farmer_profile=request.dict(),
            language=request.language
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/details/{scheme_name}")
async def get_scheme_details(
    scheme_name: str,
    language: str = Query("en", description="Response language")
):
    """Get detailed information about a specific scheme"""
    
    try:
        result = await scheme_agent.get_scheme_details(
            scheme_name=scheme_name,
            language=language
        )
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "schemes"}
