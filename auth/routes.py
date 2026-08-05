from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.database import SessionLocal
from auth.models import User
from auth.schemas import UserCreate , UserLogin , Token
from auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }

@router.post("/login", response_model=Token)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()


    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    if not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_access_token(
        {
            "user_id": existing_user.id,
            "email": existing_user.email
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }

