from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import List
class Gender(Enum):
    male = "male"
    female = "female"
class User(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str
    age: int
    gender: str
    hobbies: list[str] = []
    triggers: list[str] = []
    solutions_tried: list[str] = []
    cooling_methods: list[str] = []
    goals: list[str] = []