from typing import List, Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, EmailStr, SecretStr

class User(BaseModel):
    email: EmailStr
    password: SecretStr
    is_active: bool
    first_name: str
    last_name: str
    is_professional: bool = False


app = FastAPI(
    title="Appointment Manager",
    description="Application to manage professional appointments",
    version="0.0.1",
    contact={
        "name": "Lucas Lucyk",
        "email": "lucaslucyk@gmail.com"
    },
    license_info={
        "name": "MIT"
    }
)

users: List[User] = list()

@app.get("/users")
async def get_users():
    return users


@app.get("/users/{id}")
async def get_user(
    id: int = Path(..., description="Id to retrieve", gt=0),
    q: str = Query(None, max_length=5)
):
    return {"user": users[id], "query": q}


@app.post("/users")
async def create_user(user: User):
    users.append(user)
    return {"message": "Success", "id": users.index(user)}
