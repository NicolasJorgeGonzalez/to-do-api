from pydantic import BaseModel
from typing import List
from .task import Task

class User(BaseModel):
    id:str
    username:str
    email:str
    
class UserDB(User):
    password:str