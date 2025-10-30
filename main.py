# from typing import Union
from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["notesApp"]
collection = db["notes"]

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    collection.insert_one({"title": "Hello Mongo", "content": "Created from FastAPI"})
    notes = list(collection.find({},{"_id":0}))
    return templates.TemplateResponse(
     "index.html",{"request":request, "notes":notes}
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q:str | None = None):
    return {"item_id": item_id, "q": q}