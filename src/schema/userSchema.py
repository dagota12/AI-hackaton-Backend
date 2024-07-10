from pydantic import BaseModel, Field
from typing import List
"""
username: str = Field(...)
this 3 dots (...) aso called ellipsis it defines the implicit requirement for the field
which means   In most cases, you'll likely want to enforce
mandatory fields for essential data like usernames and passwords.
Keep the ... to ensure validation and accurate documentation.
"""

class UserBase(BaseModel):
    username: str = Field(...)
    name: str = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    hobbies: List[str] = Field(...)
    triggers: List[str] = Field(...)
    solutions_tried: List[str] = Field(...)
    cooling_methods: List[str] = Field(...)
    goals: List[str] = Field(...)

class UserCreate(UserBase):
    username: str = Field(...)
    password: str = Field(...)

    
class UserLogin(BaseModel):
    username: str = Field(...)
    password: str = Field(...)