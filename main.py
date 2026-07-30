from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UpdateUser

app = FastAPI()

db: List[User] = [
    User(id=UUID("18c8fd11-cf70-47d6-917e-9a1f282af29d"), 
         first_name="Seun", 
         last_name="Godwin",
         gender=Gender.female,
         roles=[Role.student]
         ),

    User(id=UUID("27c3ff3c-9c60-4851-a8d9-fb06b6741e87"), 
         first_name="Demian", 
         last_name="Whitehall",
         gender=Gender.male,
         roles=[Role.admin, Role.user]
         )
]




@app.get("/")
async def root():
    return {"message":"Hello world"}

@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user:User):
    db.append(user)
    return {"id": user.id}

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update:UpdateUser, user_id:UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.gender is not None:
                user.gender = user_update.gender
            if user_update.roles is not None:
                user.roles = user_update.roles
            return user
    raise HTTPException(
        status_code=404,
        detail=f"user with id:{user_id} does not exit"
    )


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return db
    raise HTTPException(
        status_code=404,
        detail=f"user with id:{user_id} does not exit"
    )




#run using python3 -m uvicorn main:app --reload (uvicorn was installed in the python environment)
#source .venv/bin/activate  