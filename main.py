from fastapi import FastAPI

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

#iniciar servidor: uvicorn main:app --reload
# ver documentacion: http://localhost:8000/docs
# ver documentacion: http://localhost:8000/redoc