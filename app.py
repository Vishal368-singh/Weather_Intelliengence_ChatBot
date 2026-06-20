import uvicorn

from Agents.agent import ask_agent
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Weather AI Agent Running"
    }

class ChatRequest(BaseModel):
    message: str
    

@app.post("/chat")
def chat(req: ChatRequest, authorization: str = Header(None)):

    answer = ask_agent(req.message, authorization)

    return {
        "response": answer
    }
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)