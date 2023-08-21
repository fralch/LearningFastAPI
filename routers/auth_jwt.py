from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

hash = "HS256" #para encriptar el token que se devuelve al usuario
access_token_expire_minutes = 1 #tiempo de expiracion del token
SECRET = "mysecret" #clave secreta para encriptar el token



crypt_context = CryptContext(schemes=["bcrypt"]) #para verificar la contraseña ingresada por el usuario con la contraseña almacenada en la base de datos


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

async def get_current_user(token: str = Depends(oauth2)):
    token_data = jwt.decode(token, SECRET, algorithms=[hash]) #decodifica el token
    username = token_data["username"] #obtiene el nombre de usuario del token

    user = search_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado", headers={"WWW-Authenticate": "Bearer"})
    return user

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    

    if not crypt_context.verify(form_data.password, user.password): #verifica que la contraseña ingresada sea la misma que la de la base de datos
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    # Generamos el token de acceso
    access_token_expires = timedelta(minutes=access_token_expire_minutes ) 

    expire = datetime.utcnow() + access_token_expires # datetime.utcnow() devuelve la fecha y hora actuales en UTC

    to_encode = {"exp": expire, "username": user.username} #creamos un diccionario con la fecha de expiracion y el nombre de usuario    

    return {"access_token": jwt.encode(to_encode, SECRET, algorithm=hash), "token_type": "bearer"}

@app.get("/users/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


"""
Los pasos para entender el funcionamiento de la autenticación JWT son los siguientes:

1. El usuario envía su nombre de usuario y contraseña al servidor.
2. El servidor verifica si el usuario existe en la base de datos.
3. El servidor verifica si la contraseña ingresada por el usuario coincide con la contraseña almacenada en la base de datos.
    - from passlib.context import CryptContext: desencrypta la contraseña almacenada en la base de datos y la compara con la contraseña ingresada por el usuario.
4. Si la contraseña es correcta, el servidor genera un token de acceso y lo devuelve al usuario.
5. El usuario almacena el token de acceso y lo envía en cada solicitud al servidor.
6. El servidor verifica si el token de acceso es válido y, si es así, devuelve los datos solicitados al usuario.
    - from jose import JWTError, jwt: decodifica el token de acceso y verifica que no haya expirado.



"""