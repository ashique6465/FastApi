from fastapi import APIRouter,FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates 
from models.note import Note 
from config.db import conn
from schemas.note import noteEntity, notesEntity
from bson.objectid import ObjectId

note = APIRouter()
templates = Jinja2Templates(directory="templates")
collection = conn["notes"]

@note.get("/", response_class=HTMLResponse)
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


@note.post("/", response_class = HTMLResponse)
async def add_note(request: Request, title: str = Form(...),desc: str = Form(...)):
    collection.insert_one({"title":title, "content":desc,"important": False})
    return RedirectResponse(url = '/', status_code = 303)

@note.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# Support both DELETE (for API/JS) and POST (so HTML forms can call the delete URL)
@note.delete("/delete/{id}")
@note.post("/delete/{id}")
async def delete_note(id: str):

    try:
        oid = ObjectId(id)
    except Exception:
        # invalid id string; redirect back
        return RedirectResponse(url='/', status_code=303)

    collection.delete_one({"_id": oid})
    return RedirectResponse(url='/', status_code=303)
