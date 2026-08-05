from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from auth.database import SessionLocal
from auth.models import User
from auth.security import SECRET_KEY, ALGORITHM


oauth2_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    credentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    user = db.query(User).filter(
        User.id == user_id
    ).first()


    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    return user