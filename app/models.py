from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, func
from sqlalchemy.sql import func
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    # datetime = timestamp
    creation_date = Column(DateTime, default=func.now(), nullable=False)

    due_date = Column(Date, nullable=True)
    # true false
    completed = Column(Boolean, default=False, nullable=False)

    completed_at = Column(DateTime, nullable=True)