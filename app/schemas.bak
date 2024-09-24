from pydantic import BaseModel
from datetime import datetime

# Schéma de base pour un utilisateur (lecture/écriture de données communes)
class UserBase(BaseModel):
    nom: str
    email: str

# Schéma pour la création d'un utilisateur (avec mot de passe)
class UserCreate(UserBase):
    password: str  # À hasher lors de la création

# Schéma pour la mise à jour d'un utilisateur (sans mot de passe)
class UserUpdate(UserBase):
    pass

# Schéma pour la réponse renvoyée par l'API (inclut des informations en lecture seule comme uid et creation_date)
class User(UserBase):
    uid: int
    creation_date: datetime

    class Config:
        orm_mode = True  #