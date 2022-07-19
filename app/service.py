from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.schema import (ErrorResponseModel, ResponseModel, UserSchema, UpdateUserModel)
from app.database import user_collection, user_helper
from bson.objectid import ObjectId

router = APIRouter()


@router.get("/hello-world")
async def root():
    return {"message": "Hello World"}

@router.post("/", response_description="Student data added into the database")
async def add_user(student: UserSchema = Body(...)):
    user_request = jsonable_encoder(student)
    user = await user_collection.insert_one(user_request)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return ResponseModel(user_helper(new_user), "Student added successfully.")

@router.get("/", response_description="Students retrieved")
async def get_students():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))

    if users:
        return ResponseModel(users, "Students data retrieved successfully")
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT) 


@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return ResponseModel(user_helper(user), "Student data retrieved successfully")
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT) 

@router.put("/{id}")
async def update_student_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    if len(req) < 1:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": req}
        )
        if updated_user:
            return ResponseModel(
                "Student with ID: {} name update is successful".format(id),
                "Student name updated successfully",
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problema na atualizacao")

    
@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return ResponseModel("Student with ID: {} removed".format(id), "Student deleted successfully")
    
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)    