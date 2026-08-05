from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from auth.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    documents = relationship(
        "Document",
        back_populates="user"
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )



from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    filename = Column(
        String
    )

    filepath = Column(
        String
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    user = relationship(
        "User",
        back_populates="documents"
    )    