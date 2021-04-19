from fastapi import APIRouter, HTTPException, Response, Depends
from app.models import User
from app.database import db
from app.auth import pwd_context, create_access_token, bearer_scheme, get_user

router = APIRouter(tags=["auth"])


@router.post("/token")
async def token_route(username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    access_token_data = {"user": {"id": user.id, "username": user.username, "admin": user.admin}}
    access_token = create_access_token(access_token_data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_user(username: str, password: str):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=401, detail='Username already exists')
    user = User(username, pwd_context.hash(password))
    db.add(user)
    db.commit()
    return Response('Created User.', 201)

@router.get('/authenticated')
async def test_authenication(_=Depends(get_user)):
    return "true"
