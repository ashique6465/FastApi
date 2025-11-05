import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# export mongouri and conn as requested
mongouri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
if mongouri == "mongodb://localhost:27017":
    print("Warning: MONGO_URI not set, using default mongodb://localhost:27017")

_client = MongoClient(mongouri)
conn = _client["notesApp"]  # conn is the database object