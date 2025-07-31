from fastapi import FastAPI
from routers import auth, task, user

app = FastAPI()

app.include_router(auth.router)
app.include_router(task.router)
app.include_router(user.router)