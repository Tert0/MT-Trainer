from fastapi import APIRouter, HTTPException, Response, Depends
from app.models import User, Evaluation
from app.database import db
from app.auth import get_user

router = APIRouter(tags=["rank"])

def calculatePoints(evaluations: list[Evaluation]):
    raw_points = 0
    raw_count = 0
    for evaluation in evaluations:
        raw_points += evaluation.points
        raw_count += evaluation.count
    percent = raw_points/raw_count*100
    points = round((raw_points/10)*percent)
    return points


@router.get("/rank/get")
async def rank_get(user=Depends(get_user)):
    users_db = db.query(User).all()
    ranklist = []
    for user in users_db:
        evaluations = db.query(Evaluation).filter(Evaluation.user_id == user.id).all()
        ranklist.append({'username': user.username,
                         'points': calculatePoints(evaluations)})
    return ranklist
