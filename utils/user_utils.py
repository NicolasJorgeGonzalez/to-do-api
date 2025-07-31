from fastapi import HTTPException, status
from bson import ObjectId

from db.client import db
from db.schemas.user import user_schema

def src_username(username:str):
  user = user_schema(db.users.find_one({"username":username}))
  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
  else:
    return user
  
def src_id(id:str):# -> None | dict[str, Any]:
  user = user_schema(db.users.find_one({"_id":ObjectId(id)}))
  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
  else:
    return user