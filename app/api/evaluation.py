from fastapi import APIRouter, Depends
from app.models import Evaluation
from app.database import db
from app.auth import get_user

router = APIRouter(tags=["evaluation"])


@router.get('/evaluations/get')
async def evaluations_get(user=Depends(get_user)):
    evaluations = db.query(Evaluation).filter(Evaluation.user_id == user.id).order_by(Evaluation.points.desc()).all()
    return [
        {
            "factor1": evaluation.factor1,
            "factor2": evaluation.factor2,
            "points": evaluation.points,
            "count": evaluation.count,
        }
        for evaluation in evaluations
    ]
