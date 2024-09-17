from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=True)

    # Timestamp de création avec DateTime
    creation_date = Column(DateTime, default=func.now(), nullable=False)

    # Date spécifique pour la tâche (ex: échéance)
    due_date = Column(Date, nullable=True)
