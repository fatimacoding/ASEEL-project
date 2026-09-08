from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def say_hello():
    return {"message": "Hello from routes!"}
from fastapi import APIRouter
from pydantic import BaseModel
from workflow.graph import ask

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    history: str = ""

@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    result = ask(request.prompt, request.history)
    return result