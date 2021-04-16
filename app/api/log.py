from fastapi import APIRouter
from app.models import LogEntry
from app.database import db


router = APIRouter(tags=["log"])


@router.post('/log/add')
async def log_add(factor1: int, factor2: int, user_result: int, duration: int):
    db.add(LogEntry(0, factor1, factor2, user_result, factor1 * factor2 == user_result, duration))
    db.commit()
    return {
        'message': 'Created Log',
        'status': 201
    }


@router.get('/log/get')
async def log_get():
    result: list[LogEntry] = db.query(LogEntry).filter(LogEntry.user_id == 0).all()
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


