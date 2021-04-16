from fastapi import APIRouter, Depends
from app.models import LogEntry, User
from app.database import db
from app.auth import get_user

router = APIRouter(tags=["log"])


@router.post('/log/add')
async def log_add(factor1: int, factor2: int, user_result: int, duration: int, user=Depends(get_user)):
    user_db = db.query(User).filter(User.id == user.id).first()
    db.add(LogEntry(user_db, factor1, factor2, user_result, factor1 * factor2 == user_result, duration))
    db.commit()
    return {
        'message': 'Created Log',
        'status': 201
    }


@router.get('/log/get')
async def log_get(user=Depends(get_user)):
    result: list[LogEntry] = db.query(LogEntry).filter(LogEntry.user_id == user.id).all()
    return [
        {
            'id': row.id,
            'factor1': row.factor1,
            'factor2': row.factor2,
            'user_result': row.user_result,
            'correct': row.correct,
            'timestamp': row.timestamp,
            'duration': row.duration
        }
        for row in result
    ]


