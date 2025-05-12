from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI(title="User Profile API")

# Pydantic model for response
class UserProfile(BaseModel):
    id: int
    name: str
    email: EmailStr

# Mock user data
MOCK_USERS = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
}

@app.get("/users/{user_id}", response_model=UserProfile)
def get_user(user_id: int):
    user = MOCK_USERS.get(user_id)
    if not user:
        return {"error": "User not found"}
    return user