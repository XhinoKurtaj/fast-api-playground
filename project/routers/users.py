from typing import List
from fastapi import APIRouter, HTTPException, status
from project.models.user import User, UserCreate
from project import db

router = APIRouter()

@router.get('/')
async def all() -> List[User]:
    return list(db.users.values())

