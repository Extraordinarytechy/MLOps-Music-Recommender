from fastapi import APIRouter, HTTPException
from melorec.api import schemas
from melorec.models import predict
from typing import List

router = APIRouter()

@router.get("/health", response_model=schemas.HealthResponse)
def health_check():
    return {"status": "ok"}


@router.post("/recommend/{user_id}", response_model=schemas.RecommendationResponse)
def get_recommendations(user_id: str):
    try:
        recommendations = predict.generate_recommendations(user_id=user_id, n=10)
        
        return {
            "user_id": user_id,
            "recommendations": recommendations
        }
    
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")