from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI(title="User Creation API")

# Pydantic model for request body
class UserCreate(BaseModel):
    name: str
    email: EmailStr

# Pydantic model for response
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

# Mock in-memory database
MOCK_USERS = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
}
next_id = 3

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    global next_id
    new_user = {"id": next_id, "name": user.name, "email": user.email}
    MOCK_USERS[next_id] = new_user
    next_id += 1
    return new_user