from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from .. import models
from ..database import get_db
from passlib.context import CryptContext
from datetime import timedelta
from ..token import create_access_token, verify_token  # Import the token functions
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # This will extract the token from the Authorization header

# Function to hash the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# User Signup Route
@router.post("/signup")
def create_user(
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        repeat_password: str = Form(...),
        db: Session = Depends(get_db)
):
    # Check if the user already exists
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Verify that passwords match
    if password != repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Hash the password using passlib
    hashed_password = hash_password(password)

    new_user = models.User(
        nom=name,
        email=email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/login", status_code=302)


# User Login Route (returns JWT token)
@router.post("/login")
def login(
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create a JWT token upon successful login
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# Protected Route to get the current user based on JWT token
@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token and extract the user info
    payload = verify_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
