from fastapi import APIRouter, Depends, Form, HTTPException, status
from datetime import date, datetime, time
from bson import ObjectId
from pymongo import ReturnDocument

from db.client import db
from db.models.user import User, UserDB
from db.models.task import Task
from db.schemas.task import task_schema
from utils.auth_utils import verify_token_access
from utils.task_utils import src_task_id

router = APIRouter(
    prefix="/task"
)

@router.post("/create")
async def create_task(task_name:str = Form(...), task_date:date = Form(...), user:User = Depends(verify_token_access)):
    task_json = {
        "user_id":user.id,
        "name":task_name,
        "date_to_complete":datetime.combine(task_date, time.min),
        "check":False
    }
    
    inserted_id = db.tasks.insert_one(task_json).inserted_id
    
    inserted_task = src_task_id(str(inserted_id))
    
    return Task(**inserted_task)

@router.delete("/delete/{task_id}")
async def delete_task(task_id:str, user:User = Depends(verify_token_access)):
    task = src_task_id(task_id)
    
    if task["user_id"] == user.id:
        deleted_task = db.tasks.find_one_and_delete({"_id":ObjectId(task_id)})
        try:
            src_task_id(task_id)
        except:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="Tarea eliminada correctamente")
    
@router.put("/update/{id}")
async def update_task(id:str, name:str = Form(...), task_date:date = Form(...), check:int = Form(...), auth:User = Depends(verify_token_access)):
    try:
        task = src_task_id(id)
        new_task = {
            "id":task["id"],
            "user_id":task["user_id"],
            "name":name,
            "date_to_complete":datetime.combine(task_date, time.min),
            "check":bool(check)
        }
    
        replaced_task = db.tasks.find_one_and_replace({"_id":ObjectId(id)}, new_task, return_document = ReturnDocument.AFTER)
        if not replaced_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro la tarea")
        return Task(**task_schema(replaced_task))
    except HTTPException as exception:
        raise exception
    
@router.put("/completed/{id}")
async def completed_task(id:str, auth:User = Depends(verify_token_access)):
    try:
        task = src_task_id(id)
        new_task = {
            "id":task["id"],
            "user_id":task["user_id"],
            "name":task["name"],
            "date_to_complete":task["date_to_complete"],
            "check":bool(1)
        }
    
        replaced_task = db.tasks.find_one_and_replace({"_id":ObjectId(id)}, new_task, return_document = ReturnDocument.AFTER)
        if not replaced_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro la tarea")
        return Task(**task_schema(replaced_task))
    except HTTPException as exception:
        raise exception