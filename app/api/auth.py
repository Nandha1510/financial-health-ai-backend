from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import crud
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.validators import validate_email, validate_password

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/register")
def register_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    validate_email(credentials.email)
    validate_password(credentials.password)

    existing_user = crud.get_user_by_email(db, credentials.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pwd = hash_password(credentials.password)
    user = crud.create_user(db, credentials.email, hashed_pwd)

    return {
        "message": "User registered successfully",
        "user_id": user.id
    }

@router.post("/login")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        subject=user.email,
        expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
