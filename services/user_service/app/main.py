from fastapi import FastAPI, HTTPException, Depends
from .models import User, UserCreate, UserUpdate
from .database import get_db
from arango import ArangoClient
from typing import List

app = FastAPI(title="User Service")

@app.get("/users/", response_model=List[User])
async def get_users(db=Depends(get_db)):
    try:
        users_collection = db.collection('users')
        users = [User(**user) for user in users_collection.all()]
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db=Depends(get_db)):
    try:
        users_collection = db.collection('users')
        user_dict = user.dict()
        result = users_collection.insert(user_dict)
        user_dict["_key"] = result["_key"]
        return User(**user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, db=Depends(get_db)):
    try:
        users_collection = db.collection('users')
        user = users_collection.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserUpdate, db=Depends(get_db)):
    try:
        users_collection = db.collection('users')
        if not users_collection.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        user_dict = user_update.dict(exclude_unset=True)
        users_collection.update_match({"_key": user_id}, user_dict)
        return User(**users_collection.get(user_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}")
async def delete_user(user_id: str, db=Depends(get_db)):
    try:
        users_collection = db.collection('users')
        if not users_collection.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        users_collection.delete(user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
