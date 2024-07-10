from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
import os
import jwt
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from database.database import get_db
from schema.userSchema import UserLogin
from schema.userSchema import UserBase

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_user(user_id):
    return {"user_id": 1, "username": "admin"}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Fetch the user from the database using the user_id
        user = await get_user(user_id)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
async def authenticate_user(creditential:UserLogin):
    # Implement DB user authentication logic here for now just an example
    if creditential.username == "admin" and creditential.password == "password":
        return {"user_id": 1, "username": "admin"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/login")
async def login(creditential: UserLogin,db: AsyncIOMotorClient = Depends(get_db)):
    user = await authenticate_user(creditential)
    access_token = create_access_token(data={"user_id": user["user_id"]})
    return {"access_token": access_token, "token_type": "bearer"}
@router.post("/register")
async def register(user:UserBase,db: AsyncIOMotorClient = Depends(get_db)):
    # Implement DB user registration logic here for now just an example
    return {"message": "User registered successfully"}