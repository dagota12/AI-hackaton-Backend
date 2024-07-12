import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import pymongo
from fastapi import HTTPException, status
load_dotenv() #load enviromental variables
MONGODB_URI = os.getenv("DB_URI")
# print(MONGODB_URI)

async def get_db():
    try:
        client = MongoClient(MONGODB_URI)
        db = client["mindfull-recovery"]  # Connect to the database
        return db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect to database: {e}"
        )



