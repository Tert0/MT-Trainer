from fastapi import APIRouter
from app.models import Evaluation
from app.database import db

router = APIRouter(tags=["evaluation"])


@router.get('/evaluations/get')
async def evaluations_get():
    evaluations = db.query(Evaluation).filter(Evaluation.user_id == 0).order_by(Evaluation.points.desc()).all()
    return [
        {
            "factor1": evaluation.factor1,
            "factor2": evaluation.factor2,
            "points": evaluation.points,
            "count": evaluation.count,
        }
        for evaluation in evaluations
    ]
