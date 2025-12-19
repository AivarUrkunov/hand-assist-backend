import os
import requests
from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aivarurkunov.github.io",  # GitHub Pages origin
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.get("/")
def root():
    return {"ok": True, "service": "hand-assist-backend"}

@app.get("/send_test")
def send_test():
    if not BOT_TOKEN or not CHAT_ID:
        raise HTTPException(status_code=500, detail="Missing BOT_TOKEN or CHAT_ID")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "Hand Assist: backend connected ✅"}

    r = requests.post(url, json=payload, timeout=15)
    if not r.ok:
        raise HTTPException(status_code=500, detail=r.text)

    return {"ok": True}

from pydantic import BaseModel

class TaskIn(BaseModel):
    text: str

@app.post("/task")
def create_task(task: TaskIn):
    if not BOT_TOKEN or not CHAT_ID:
        raise HTTPException(status_code=500, detail="Missing BOT_TOKEN or CHAT_ID")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"New task: {task.text}"}

    r = requests.post(url, json=payload, timeout=15)
    if not r.ok:
        raise HTTPException(status_code=500, detail=r.text)

    return {"ok": True}
