from fastapi import APIRouter, HTTPException, status, Form, Depends
from bson import ObjectId

from db.client import db
from db.models.user import User, UserDB
from db.schemas.task import task_schema, task_schema_list
from db.schemas.user import user_schema
from utils.auth_utils import verify_token_access, hash_password
from utils.user_utils import src_username, src_id

router = APIRouter(
    prefix="/user"
)

@router.get("/me")
async def user_me(user:UserDB = Depends(verify_token_access)):
    return user

@router.get("/my_tasks")
async def get_my_tasks(user:User = Depends(verify_token_access)):
    tasks = db.tasks.find({"user_id":user.id})
    list = task_schema_list(tasks)
    if len(list) == 0:
        return {"message":"No tienes tareas"}
    return list

@router.post("/register")
async def user_register(username:str = Form(...), password:str = Form(...), email:str = Form(...)):
    try:
        user = src_username(username)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Este nombre de usuario ya existe")
    except HTTPException as exception:
        if exception.status_code == status.HTTP_404_NOT_FOUND:
            user_json = {
                "username":username,
                "email":email,
                "password":hash_password(password)
            }
            inserted_id = db.users.insert_one(user_json).inserted_id
            inserted_user = src_id(str(inserted_id))
            return User(**inserted_user)
        else:
            raise exception