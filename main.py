# from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.note import note



app = FastAPI()

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    mongo_uri = "mongodb://localhost:27017"
    print("Warning: MONGO_URI not set, using default mongodb://localhost:27017")

client = MongoClient(mongo_uri)

db = client["notesApp"]
