from fastapi import Depends , HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext 
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from db.models.user import User, UserDB
from utils.user_utils import src_username

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt  = CryptContext(schemes=["bcrypt"])

SECRET_KEY = "eeae3e588203cc4c55c62ff09fe2ec7c99529c3bd58b4de45a9b0cb9fffa67a6" # -> openssl rand -hex 32
ALGORITHM  = "HS256"
TOKEN_TIME_DURATION = 60 # minutes

def hash_password(password:str):
  return crypt.hash(password)

def verify_password(password:str, hashed_password:str):
    return crypt.verify(password, hashed_password)

def auth(username:str, password:str):
    try:
      user = src_username(username)
      if not verify_password(password, user["password"]):
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta")
      return User(**user)
    except HTTPException as exception:
      if exception.status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario incorrecto")
      else:
        raise exception

def create_token_access(username:str):
    try:
        json = {
          "sub":username,
          "exp":datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TIME_DURATION)
      }
        return jwt.encode(json, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError as exception:
      raise exception

async def verify_token_access(token:str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
    try:
      decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM, options={"verify_exp": True})
      if decoded_token == None:
        raise exception
      try:
        user = src_username(decoded_token["sub"])
      except HTTPException as exception2:
          raise exception2
    except JWTError:
      raise exception

    return User(**user)