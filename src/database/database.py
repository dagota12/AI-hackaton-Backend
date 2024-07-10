import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from fastapi import HTTPException, status
load_dotenv() #load enviromental variables
MONGODB_URI = os.getenv("DB_URI")
print(MONGODB_URI)
client = AsyncIOMotorClient(MONGODB_URI)

async def get_db():
    """
    Function to establish an asynchronous connection to the MongoDB database.

    Returns:
        AsyncIOMotorClient: An instance of the database client if successful.
        Raises:
            HTTPException: If an error occurs while connecting to the database.
    """
    try:
        db = client["mindfull-recovery"] # Connect to the database
        yield db  # Yield the database object
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect to database: {e}"
        )



