from fastapi import FastAPI, HTTPException
from routers import users, products
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(users.router)
app.include_router(products.router)
app.mount("/estaticos", StaticFiles(directory="static"), name="static") #para que se vean las imagenes la ruta es: http://localhost:8000/imagenes/


@app.get("/")
async def root():
    return {"message": "Hello World"}



#iniciar servidor: uvicorn main:app --reload
# ver documentacion: http://localhost:8000/docs
# ver documentacion: http://localhost:8000/redoc