from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    creation_date = Column(DateTime, default=func.now(), nullable=False)

    # Ajout de la relation avec les tâches
    tasks = relationship("Task", back_populates="user")  # Relation avec la table Task


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    creation_date = Column(DateTime, default=func.now(), nullable=False)
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Clé étrangère vers la table User
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=False)

    # Relation inverse vers l'utilisateur
    user = relationship("User", back_populates="tasks")