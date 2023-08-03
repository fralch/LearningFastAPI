from fastapi import APIRouter, HTTPException

router = APIRouter( tags=["items"]  )


# Path; "http://localhost:8000/items/1"
@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Query: "http://localhost:8000/items/?item_id=1&q=string"
@router.get("/items/")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@router.post("/user/", status_code=201) # response_model=User: para que devuelva el objeto creado
async def create_user(user: str):
    return user

@router.put("/items/{item_id}")
async def update_item(item_id: int, item: str):
    raise HTTPException(status_code=204, detail="Item ")
    # return {"item_name": item.name, "item_id": item_id}

@router.patch("/items/{item_id}")
async def update_item(item_id: int, item: str):
    return {"item_name": item.name, "item_id": item_id}

@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"item_id": item_id}

