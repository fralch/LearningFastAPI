from fastapi import FastAPI, HTTPException
from routers import users

app = FastAPI()

#Routers
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}



#iniciar servidor: uvicorn main:app --reload
# ver documentacion: http://localhost:8000/docs
# ver documentacion: http://localhost:8000/redoc