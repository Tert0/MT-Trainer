from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Depends
from collections import namedtuple
from dotenv import load_dotenv
from fastapi.security import HTTPBearer
load_dotenv()
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 24 * 5))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bearer_scheme = HTTPBearer()


def get_token(token=Depends(bearer_scheme)):
    return str(token.credentials)


def create_access_token(data: dict, expires_delta=None):
    data = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(token: str = Depends(get_token)):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.exceptions.InvalidTokenError as e:
        if isinstance(e, jwt.exceptions.ExpiredSignatureError):
            raise HTTPException(status_code=401, detail='Token is expired')
        else:
            raise HTTPException(status_code=401, detail='Token is invalid')
    data_struct = namedtuple('user', data['user'].keys())
    user = data_struct(**data['user'])
    return user
