from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
#from mangum import Mangum

app = FastAPI()
#handler = Mangum(app)

# In-memory storage for user data
db = [{
    "id": "1234",
    "name": "Adi",
    "email": "AB@gmail.com",
    "password": "AB123"
}]

# User model using Pydantic to enforce data types and constraints
class User(BaseModel):
    id: str
    name: str
    email: str
    password: str

@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.get("/users", response_model=List[User])
async def find_all_users():
    return db

@app.get("/users/{user_id}", response_model=User)
async def find_one_user(user_id: str):
    user = next((user for user in db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: User):
    db.append(user.dict())
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: User):
    user_index = next((index for index, user in enumerate(db) if user['id'] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Update user details
    db[user_index].update(user_update.dict(exclude_unset=True))
    return db[user_index]

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str):
    user_index = next((index for index, user in enumerate(db) if user['id'] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.pop(user_index)
    return {"message": "User deleted successfully"}

