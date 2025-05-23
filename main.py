from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="Rasa Chatbot API", description="FastAPI wrapper for Rasa", version="1.0")

# Tambahkan CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify the Express origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

RASA_URL = "http://localhost:5005/webhooks/rest/webhook" 
# 🎯 Model untuk request body
class UserMessage(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Rasa!"}

@app.post("/chat/", summary="Kirim pesan ke Rasa", response_description="Respons dari Rasa")
def chat_with_rasa(user_message: UserMessage):
    """
    Kirim pesan ke Rasa dan kembalikan respons chatbot-nya.

    Contoh request body:
    {
        "message": "Halo, apa kabar?"
    }
    """
    response = requests.post(
        RASA_URL,
        json={"sender": "user", "message": user_message.message}
    )
    return response.json()
