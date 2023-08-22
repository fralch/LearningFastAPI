from fastapi import APIRouter, HTTPException
from db.models.user import UserModel as User
from db.schemas.user_schema import user_schema, users_schema
from db.cliente import db_client

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
    return False
    

@router.patch("/{id}")
async def update_item(item_id: int, item: str):
    return {"item_name": item.name, "item_id": item_id}

@router.delete("/{id}")
async def delete_item(item_id: int):
    return {"item_id": item_id}

