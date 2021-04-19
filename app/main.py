from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import db
import uvicorn
from redis import Redis
from app.api import evaluation, log, exercise, auth, rank
from app.auth import get_user
from dotenv import load_dotenv

load_dotenv()
import os

ENV_RELOAD = bool(os.getenv('RELOAD', "False"))
ENV_PORT = int(os.getenv('PORT', 80))

app = FastAPI()

app.include_router(auth.router)
app.include_router(evaluation.router)
app.include_router(log.router)
app.include_router(exercise.router)
app.include_router(rank.router)

redis = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379))

db.Base.metadata.create_all(db.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/secret")
async def secret(user=Depends(get_user)):
    return f'Hello {user.username}!'


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=ENV_PORT, reload=ENV_RELOAD)
