import os
from dotenv import load_dotenv
from database.database import get_db
from fastapi import FastAPI, APIRouter,Depends
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from schema.userSchema import UserLogin
from auth.auth import router as auth_router
from routes.users import router as users_router

load_dotenv() #load enviromental variables
DB_URI = os.getenv("DB_URI")
print(DB_URI)

app = FastAPI()

# Add your routes here
app.include_router(auth_router)
app.include_router(users_router)


