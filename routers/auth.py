# Importamos las bibliotecas FastAPI y HTTPException, que nos permiten crear una API web rápida.
# También importamos BaseModel de pydantic, que es una biblioteca para validación de datos.
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #para autenticacion

# Creamos una instancia de la aplicación FastAPI.
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
        "password": "123456",
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@gmai.com",
        "disabled": True,
        "password": "secret",
    },
}

# Definimos una función llamada "search_user" que busca un usuario en la base de datos según su nombre de usuario.
# Recibe como parámetro el nombre de usuario (username) que se desea buscar.
def search_user(username: str):
    # Paso 1: Verificar si el nombre de usuario existe en la base de datos.
    if username in user_db:
        # Paso 2: Si el nombre de usuario existe, obtenemos los detalles del usuario como un diccionario.
        user_details = user_db[username]

        # Paso 3: Ahora, vamos a crear una instancia del objeto UserInDB utilizando los detalles del usuario.
        # Para hacer esto, desempaquetamos el diccionario usando ** para pasar sus elementos como argumentos individuales.
        user_instance = UserInDB(**user_details)

        # Paso 4: Hemos creado una hoja especial que contiene todos los detalles del usuario.
        # Ahora, podemos devolver esa hoja especial para que otros puedan ver la información del usuario.
        return user_instance

    # Paso 5: Si el nombre de usuario no está en la base de datos, no podemos encontrar al usuario.
    # En este caso, devolvemos None para indicar que el usuario no existe en la base de datos.
    return None

async def get_current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado", headers={"WWW-Authenticate": "Bearer"})
    return user

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    if user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    return {"access_token": user.username, "token_type": "bearer"}

# Definimos una ruta llamada "/users/{username}" que recibe el nombre de usuario como parámetro.
# Esta ruta devuelve los detalles del usuario si el usuario existe en la base de datos.
@app.get("/users/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

