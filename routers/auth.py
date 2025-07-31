from fastapi import APIRouter, Depends , HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from utils.auth_utils import *

router = APIRouter()

# chequear si el usuario es correcto y devolver un token en caso de serlo
@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    try:
        user  = auth(form.username, form.password)
        token = create_token_access(user.username)
        return {"token_access": token, "token_type":"bearer"}
    except HTTPException as exception:
        raise exception