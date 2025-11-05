# from typing import Union
from fastapi import FastAPI, Request, Form

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    mongo_uri = "mongodb://localhost:27017"
    print("Warning: MONGO_URI not set, using default mongodb://localhost:27017")

client = MongoClient(mongo_uri)

db = client["notesApp"]
collection = db["notes"]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    # Include _id so we can convert it to string for templates/JSON
    docs = list(collection.find({}, {"_id": 1, "title": 1, "content": 1}))

    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc.get("_id")),
            "title": doc.get("title", ""),
            "content": doc.get("content", "")
        })

    return templates.TemplateResponse(
        "index.html", {"request": request, "newDocs": newDocs}
    )

@app.post("/", response_class = HTMLResponse)
async def add_note(request: Request, title: str = Form(...),desc: str = Form(...)):
    collection.insert_one({"title":title, "content":desc})
    return RedirectResponse(url = '/', status_code = 303)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}