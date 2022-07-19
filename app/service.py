from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.schema import (ErrorResponseModel, ResponseModel, UserSchema, UpdateUserModel)
from app.database import add_user, get_all_users, get_user_by_id, update_user, delete_user
from bson.objectid import ObjectId

router = APIRouter()


@router.get("/hello-world")
async def root():
    return {"message": "Hello World"}

@router.post("/", response_description="user data added into the database")
async def add_user(user: UserSchema = Body(...)):
    user_request = jsonable_encoder(user)
    new_user = await add_user(user_request)
    return ResponseModel(new_user, "user added successfully.")

@router.get("/", response_description="users retrieved")
async def get_users():
    users = await get_all_users()

    if users:
        return ResponseModel(users, "users data retrieved successfully")
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT) 


@router.get("/{id}", response_description="user data retrieved")
async def get_user_data(id):
    user = await get_user_by_id(id)
    if user:
        return ResponseModel(user, "user data retrieved successfully")
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT) 

@router.put("/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    
    if updated_user:
        return ResponseModel(
            "user with ID: {} name update is successful".format(id),
            "user name updated successfully",
        )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problema na atualizacao")

    
@router.delete("/{id}", response_description="user data deleted from the database")
async def delete_user_data(id: str):
    delete_user = await delete_user(id)
    
    if delete_user:
        return ResponseModel("user with ID: {} removed".format(id), "user deleted successfully")
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)    