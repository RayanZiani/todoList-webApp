from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .token import verify_token
from .models import User
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"Token received in get_current_user: {token}")  # Debugging

    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")

    try:
        payload = verify_token(token)
        user_id = payload.get("sub")  # Le "sub" contient l'UID de l'utilisateur
        print(f"Decoded token payload: {payload}")
        print(f"Looking for user with UID: {user_id}")

        # Utiliser "uid" au lieu de "id" pour trouver l'utilisateur dans la base de données
        user = db.query(User).filter(User.uid == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")