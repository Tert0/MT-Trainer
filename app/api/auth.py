from fastapi import APIRouter, HTTPException, Response, Depends
from app.models import User
from app.database import db
from app.auth import pwd_context, create_access_token, bearer_scheme, get_user
from datetime import timedelta
from redis import Redis
import os
import jwt

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

router = APIRouter(tags=["auth"])

redis = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379))

@router.post("/token")
async def token_route(username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    access_token_data = {"user": {"id": user.id, "username": user.username, "admin": user.admin}}
    access_token = create_access_token(access_token_data)
    refresh_token = create_access_token({'userid': user.id}, timedelta(minutes=60*24))
    redis.lpush('refresh_tokens', refresh_token)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


@router.post("/register")
async def register_user(username: str, password: str):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=409, detail='Username already exists')
    user = User(username, pwd_context.hash(password))
    db.add(user)
    db.commit()
    return Response('Created User.', 201)

@router.post('/refresh')
async def refresh_route(refresh_token: str):
    refresh_tokens = redis.lrange('refresh_tokens', 0, redis.llen('refresh_tokens'))
    if refresh_token.encode('utf-8') not in refresh_tokens:
        print('NOT IN CACHE')
        raise HTTPException(status_code=401, detail='Invalid Refresh Token')
    try:
        refresh_data = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.exceptions.InvalidTokenError as e:
        if isinstance(e, jwt.exceptions.ExpiredSignatureError):
            raise HTTPException(status_code=401, detail='Refresh Token is expired')
        else:
            raise HTTPException(status_code=401, detail='Refresh Token is invalid')
    user = db.query(User).filter(User.id == refresh_data['userid']).first()
    access_token_data = {"user": {"id": user.id, "username": user.username, "admin": user.admin}}
    access_token = create_access_token(access_token_data)
    return {"access_token": access_token, "token_type": "bearer"}



@router.get('/authenticated')
async def test_authenication(_=Depends(get_user)):
    return "true"
