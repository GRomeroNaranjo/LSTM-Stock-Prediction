from fastapi import FastAPI
from app import crud 
from app import database as db

app = FastAPI()

db.init_db()

@app.get("/")
async def index():
    return {"message": "Welcome to the Sociloc Web Application"}


@app.post("/user")
async def create_user(username: str, emai: str, full_name: str, password: str):
    user = crud.create_user(username, emai, full_name, password)
    return {"user": user}

@app.put("/user/update")
async def update_user(id: int, username: str, email: str, full_name: str, password: str):
    user = crud.update_user(id, username, email, full_name, password)
    return {"user": "user"}

@app.get("/user/read")
async def get_user(id: int):
    user = get_user(id)
    return {"user": user}

@app.get("/user/delete")
async def index(id: int):
    user = crud.delete_user(id)
    return {"user": user}