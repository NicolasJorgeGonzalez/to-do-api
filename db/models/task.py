from pydantic import BaseModel
from datetime import date

class Task(BaseModel):
    id:str
    user_id:str
    name:str
    date_to_complete:date
    check:bool