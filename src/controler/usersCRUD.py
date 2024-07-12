from typing import List
from fastapi import HTTPException, status
from models.users import User
from database.database import get_db
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from schema.userSchema import UserBase,UserLogin
async def create_user(db: AsyncIOMotorClient, user: UserBase):
    user_data = user.dict()
    try:
        result = await db["users"].insert_one(user_data)
        return result.inserted_id
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    except Exception as e:
        # Handle other potential errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {e}",
        )