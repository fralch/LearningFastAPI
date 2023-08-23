import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv() # Carga las variables de entorno desde el archivo .env
# DBLocal
# db_client = MongoClient('localhost', 27017).local 

# DBAtlas
db_client = MongoClient(os.environ["MONGO_ATLAS"]).test