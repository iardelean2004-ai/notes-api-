from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

notes = []
next_id = 1


class NoteCreate(BaseModel):
    title: str
    content: str


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.post("/notes")
def create_note(note: NoteCreate):
    global next_id
    new_note = {"id": next_id, "title": note.title, "content": note.content}
    notes.append(new_note)
    next_id += 1
    return new_note


@app.get("/notes")
def list_notes():
    return notes


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Notița nu există")


@app.put("/notes/{note_id}")
def update_note(note_id: int, data: NoteCreate):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = data.title
            note["content"] = data.content
            return note
    raise HTTPException(status_code=404, detail="Notița nu există")


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return {"message": "Notița a fost ștearsă"}
    raise HTTPException(status_code=404, detail="Notița nu există")


