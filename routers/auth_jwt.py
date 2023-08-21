from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import JWTError, jwt
from passlib.context import CryptContext

Hash = "HS256" #para encriptar el token que se devuelve al usuario

crypt_context = CryptContext(schemes=["bcrypt"]) #para encriptar la contraseña del usuario


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login") #para autenticacion

# Definimos una clase "User" que hereda de "BaseModel".
# Esta clase representa el modelo de datos para un usuario y define sus atributos.
class User(BaseModel):
    username: str
    full_name: str = None
    email: str
    disabled: bool = None

# Definimos otra clase "UserInDB" que hereda de "User".
# Esta clase representa el modelo de datos para un usuario en la base de datos y agrega el atributo "password".
class UserInDB(User):
    password: str

# Creamos una base de datos ficticia llamada "user_db" que contiene información de usuarios.
user_db = {
    "johndoe": {
        "username": "fralch",
        "full_name": "John Doe",
        "email": "ingfralch@gmail.com",
        "disabled": False,
        "password": "$2a$12$Lbux8mrAprbDE.izHmfo6eyDKmff06lM/.S/e9Y6A2h0t2KsS0YlS",
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@gmai.com",
        "disabled": True,
        "password": "$2a$12$Lbux8mrAprbDE.izHmfo6eyDKmff06lM/.S/e9Y6A2h0t2KsS0YlS",
    },
}

def search_user(username: str):
    if username in user_db:
        user_details = user_db[username]
        user_instance = UserInDB(**user_details)
        return user_instance
    return None


async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    

    if not crypt_context.verify(form_data.password, user.password): #verifica que la contraseña ingresada sea la misma que la de la base de datos
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    


    return {"access_token": user.username, "token_type": "bearer"}