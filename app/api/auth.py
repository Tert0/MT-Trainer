from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User
from app.database import db
from app.auth import pwd_context, create_access_token

router = APIRouter(tags=["auth"])


@router.post("/token")
async def token_route(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    access_token_data = {"user": {"id": user.id, "username": user.username, "admin": user.admin}}
    access_token = create_access_token(access_token_data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_user(form_data: OAuth2PasswordRequestForm = Depends()):
    if db.query(User).filter(User.username == form_data.username).first():
        raise HTTPException(status_code=401, detail='Username already exists')
    user = User(form_data.username, pwd_context.hash(form_data.password))
    db.add(user)
    db.commit()
    return Response('Created User.', 201)
