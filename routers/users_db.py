from fastapi import APIRouter, HTTPException
from db.models.user import UserModel as User
from db.cliente import db_client

router = APIRouter( tags=["users_db"]  )




@router.get("/")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@router.post("/crear",response_model=User , status_code=201) 
async def create_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user = db_client.local.users.find_one({"_id": id})
    return new_user

@router.put("/{id}")
async def update_item(item_id: int, item: str):
    raise HTTPException(status_code=204, detail="Item ")

@router.patch("/{id}")
async def update_item(item_id: int, item: str):
    return {"item_name": item.name, "item_id": item_id}

@router.delete("/{id}")
async def delete_item(item_id: int):
    return {"item_id": item_id}

