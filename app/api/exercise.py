from fastapi import APIRouter, Depends
from app.models import Exercises, Evaluation, User
from app.database import db
import random
from app.auth import get_user

router = APIRouter(tags=["exercise"])


async def generateExercise(user_id):
    evaluation_query = db.query(Evaluation).filter(Evaluation.user_id == user_id).order_by(Evaluation.points.asc())
    exercises = []
    if len(evaluation_query.all()) >= 3:
        for evaluation in evaluation_query.all()[:3]:
            exercises.append({"factor1": evaluation.factor1, "factor2": evaluation.factor2})
    exercises.append({"factor1": random.randint(2, 10), "factor2": random.randint(2, 10)})
    return random.choice(exercises)


@router.get('/exercise/generate')
async def generate_exercise(user=Depends(get_user)):
    factor1, factor2 = (await generateExercise(user.id)).values()
    if db.query(Exercises).filter(Exercises.user_id == user.id).first() is None:
        user_db = db.query(User).filter(User.id == user.id).first()
        db.add(Exercises(user_db, factor1, factor2))
    else:
        db.query(Exercises).filter(Exercises.user_id == user.id).update({Exercises.factor1: factor1,
                                                                            Exercises.factor2: factor2,
                                                                            Exercises.result: factor1 * factor2})
    db.commit()
    return {
        'factor1': factor1,
        'factor2': factor2
    }


@router.post('/exercise/check')
async def check_exercise(user_result: int, user=Depends(get_user)):
    exercise: Exercises = db.query(Exercises).filter(Exercises.user_id == user.id).first()
    if exercise is None:
        return {
            'status': 400,
            'message': 'Exercise does not exists'
        }
    duration = 1  # TODO Measure Duration in the backend
    points = 1 if exercise.result == user_result else 0  # TODO Calculate Points with the Duration
    evaluation = db.query(Evaluation).filter(Evaluation.user_id == 0,
                                             Evaluation.factor1 == exercise.factor1,
                                             Evaluation.factor2 == exercise.factor2).first()
    if evaluation is None:
        user = db.query(User).filter(User.id == user.id).first()
        evaluation = Evaluation(user, exercise.factor1, exercise.factor2, points)
        db.add(evaluation)
        db.commit()
    else:
        db.query(Evaluation).filter(Evaluation.id == evaluation.id).update({
            Evaluation.points: evaluation.points + points,
            Evaluation.count: evaluation.count + 1,
        })
    db.commit()
    return {
        'status': 200,
        'result': exercise.result == user_result
    }


@router.get('/exercise/get')
async def get_exercise(user=Depends(get_user)):
    print(f'USERID:{user.id}')
    exercise: Exercises = db.query(Exercises).filter(Exercises.user_id == user.id).first()
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
