from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import db
from models import LogEntry, Exercises
import uvicorn
import random
from dotenv import load_dotenv

load_dotenv()
import os

ENV_RELOAD = bool(os.getenv('REALOAD', "False"))
ENV_PORT = int(os.getenv('PORT', 80))

app = FastAPI()

db.Base.metadata.create_all(db.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/ping')
async def ping():
    return 'Pong!'


@app.post('/log/add')
async def log_add(factor1: int, factor2: int, user_result: int, duration: int):
    db.add(LogEntry(0, factor1, factor2, user_result, factor1 * factor2 == user_result, duration))
    db.commit()
    return {
        'message': 'Created Log',
        'status': 201
    }


@app.get('/log/get')
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


@app.get('/exercise/generate')
async def generate_exercise():
    factor1 = random.randint(2, 10)
    factor2 = random.randint(2, 10)
    if db.query(Exercises).filter(Exercises.user_id == 0).first() is None:
        db.add(Exercises(0, factor1, factor2))
    else:
        db.query(Exercises).filter(Exercises.user_id == 0).update({Exercises.factor1: factor1,
                                                                   Exercises.factor2: factor2,
                                                                   Exercises.result: factor1 * factor2})
    db.commit()
    return {
        'factor1': factor1,
        'factor2': factor2
    }


@app.post('/exercise/check')
async def check_exercise(user_result: int):
    exercise: Exercises = db.query(Exercises).filter(Exercises.user_id == 0).first()
    if exercise is None:
        return {
            'status': 400,
            'message': 'Exercise does not exists'
        }
    return {
        'status': 200,
        'result': exercise.result == user_result
    }


@app.get('/exercise/get')
async def get_exercise():
    exercise: Exercises = db.query(Exercises).filter(Exercises.user_id == 0).first()
    if exercise is None:
        return {
            'status': 400,
            'message': 'Exercise does not exists'
        }
    return {
        'status': 200,
        'exercise': {
            'factor1': exercise.factor1,
            'factor2': exercise.factor2
        }
    }



if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=ENV_PORT, reload=ENV_RELOAD)
