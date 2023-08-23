from fastapi import APIRouter, HTTPException
from db.models.user import UserModel as User
from db.schemas.user_schema import user_schema, users_schema
from db.cliente import db_client
from bson import ObjectId

router = APIRouter( prefix="/user_db", tags=["users_db"]  )

def get_user(username: str):
    user = db_client.local.users.find_one({"username": username})
    if user:
        return user
    else:
        return False


@router.get("/", response_model=list[User])
async def users():
    users = db_client.local.users.find()
    return users_schema(users)

@router.get("/{id}",  response_model=User )
async def user(id: str):
    user = db_client.local.users.find_one({"_id": ObjectId(id)})
    if user:
        return user_schema(user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/") 
async def create_user(user: User):
    user_exist = get_user(user.username)
    if user_exist:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    

    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user = db_client.local.users.find_one({"_id": id})
    #sacando el id de la respuesta
    id_mongo = str(new_user["_id"])
    #remplazando el id de mongo por el id de la respuesta 
    """
     Es como cuando se sobre escribe un valor de un objeto en javascript, pero en un diccionario de python
        JAVASCRIPT
        const myObject = {
        name: "John Doe",
        age: 30
        };

        myObject.name = "Jane Doe";

        PYTHON
        my_dict = {
        "name": "John Doe",
        "age": 30
        }

        my_dict["name"] = "Jane Doe"

    """
    new_user["_id"] =  id_mongo

    return new_user


@router.put("/{id}")
async def update_item(id: str, user: User):
    user_without_id = dict(user)
    del user_without_id["id"]
    updated_user = db_client.local.users.update_one({"_id": ObjectId(id)}, {"$set": user_without_id})
    if updated_user.modified_count == 1:
        user = db_client.local.users.find_one({"_id": ObjectId(id)})
        return user_schema(user)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
    

@router.delete("/{id}")
async def delete_item(id : str):
    borrardo = db_client.local.users.delete_one({"_id": ObjectId(id)})
    if borrardo.deleted_count == 1:
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


