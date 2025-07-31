# user es lo que nos llega de la base de datos
from db.schemas.task import task_schema_list


def user_schema(user):
    if user == None:
        return None
    else:
        return {
            "id":str(user.get("_id")),
            "username":user.get("username"),
            "email":user.get("email"),
            "password":user.get("password")
        }