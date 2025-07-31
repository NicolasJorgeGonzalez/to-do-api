from fastapi import HTTPException, status
from bson import ObjectId

from db.client import db
from db.schemas.task import task_schema

def src_task_id(id:str):
  task = task_schema(db.tasks.find_one({"_id":ObjectId(id)}))
  if task == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
  else:
    return task