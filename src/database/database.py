import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import pymongo
from fastapi import HTTPException, status
load_dotenv() #load enviromental variables
MONGODB_URI = os.getenv("ATLAS_URI")
# print(MONGODB_URI)

async def get_db():

    try:
        client = AsyncIOMotorClient(MONGODB_URI)
        db = client["mindfull-recovery"] # Connect to the database
        yield db  # Yield the database object
        # pymongo.errors.ConnectionFailure

    except pymongo.errors.ConnectionFailure as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect to database: {e}"
        )



