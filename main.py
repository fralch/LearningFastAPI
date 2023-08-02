from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Path; "http://localhost:8000/items/1"
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Query: "http://localhost:8000/items/?item_id=1&q=string"
@app.get("/items/")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/user/", status_code=201, response_model=User) # response_model=User: para que devuelva el objeto creado
async def create_user(user: User):
    return user

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    raise HTTPException(status_code=204, detail="Item ")
    # return {"item_name": item.name, "item_id": item_id}

@app.patch("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"item_id": item_id}


#iniciar servidor: uvicorn main:app --reload
# ver documentacion: http://localhost:8000/docs
# ver documentacion: http://localhost:8000/redoc