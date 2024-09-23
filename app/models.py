from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum




class RoleEnum(enum.Enum):
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Store hashed password
    creation_date = Column(DateTime, default=func.now(), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    creation_date = Column(DateTime, default=func.now(), nullable=False)
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")