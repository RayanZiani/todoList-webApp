from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connexion à la base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./todolist.db"

# Créer le moteur de base de données
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Créer une session de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer une base de données de base
Base = declarative_base()