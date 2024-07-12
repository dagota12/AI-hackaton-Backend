from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
from typing import Annotated, Union
import os
import jwt
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from database.database import get_db
from schema.userSchema import UserLogin
from schema.userSchema import UserBase,UserVerify
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from controler.usersCRUD import create_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

#tokenUrl="token" ets up the OAuth2 scheme, which expects the token to be 
# sent in the Authorization header with the prefix "Bearer ".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = .5

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
async def get_user(user_id):
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
    
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
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
        return payload
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

# sends token for the user most of the time
# user lofin credential is sent to token endpoint

@router.post("/token")
async def login(creditential: Annotated[OAuth2PasswordRequestForm, Depends()],db: AsyncIOMotorClient = Depends(get_db)):
    user = await authenticate_user(creditential)
    access_token = create_access_token(data={"user_id": user["user_id"]})
    return {"access_token": access_token, "token_type": "bearer"}
#sends token for the user
@router.post("/login")
async def login(creditential: Annotated[OAuth2PasswordRequestForm, Depends()],db: AsyncIOMotorClient = Depends(get_db)):
    user = await authenticate_user(creditential)
    access_token = create_access_token(data={"user_id": user["user_id"]})
    return {"access_token": access_token, "token_type": "bearer"}
@router.post("/register")
async def register(user: UserBase, db: AsyncIOMotorClient = Depends(get_db)):
    # check if user exists
    user_exists = await db["users"].find_one({"username": user.username})
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )

    # hashed pwd impl and other functionalities
    # Implement DB user registration logic here for now just an example
    await create_user(db, user)
    return {"message": "User registered successfully"}