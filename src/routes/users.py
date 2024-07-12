from fastapi import APIRouter, Depends, HTTPException,status
from auth.auth import get_current_user
from schema.userSchema import UserUpdate

router = APIRouter(prefix="/user",tags= ["User"])

@router.put("/profile")
def update(user: UserUpdate,current_user: dict = Depends(get_current_user)):
    return current_user