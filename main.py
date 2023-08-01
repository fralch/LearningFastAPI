from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}



#iniciar servidor: uvicorn main:app --reload
# ver documentacion: http://localhost:8000/docs
# ver documentacion: http://localhost:8000/redoc