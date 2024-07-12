from typing import List
from fastapi import HTTPException, status
from models.users import User
from database.database import get_db
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from schema.userSchema import UserBase
async def create_user(db: AsyncIOMotorClient, user: UserBase):
    user_data = user.dict()
    # Add any additional user data processing here
    result = await db["users"].insert_one(user_data)
    return result.inserted_id