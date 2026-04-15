from urllib import response

from fastapi import FastAPI,Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434",   
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/contact-us")
def read_root():
    return {"email": "suvam@gmail.com"}

# This endpoint will receive a message from the user and return a response from the model
@app.post("/chat")
def chat(
        message: str = Body(..., description="The message to send to the model")
):    
    response = client.chat(
        model="gemma:2b",
        messages=[{"role": "user", "content": message}],
    )

    return {"response": response.message.content}