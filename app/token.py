from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException

SECRET_KEY = "dwhTr_-{<x%L!8=q;2M5CE/K.kQ]JjF`usvRceXZBpS,z>@(byKB)g_[7=,TzStF;5fR/m98aA2e%G!.Qws&(Wry-?k:P6VjdYh`JBY(?2+HE^pQAU'r<ztwv;{k$/uXy3c74F5-VfW`_K>S]CT&Z#"
ALGORITHM = "HS512"  # Changed to HS512
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()


    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})


    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# Function to verify the JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
