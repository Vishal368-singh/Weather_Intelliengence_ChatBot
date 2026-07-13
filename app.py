from http.client import HTTPException
from typing import Optional
import uvicorn
from Agents.agent import ask_agent
from fastapi import FastAPI, Header
from pydantic import BaseModel

from Utils.context import current_token

app = FastAPI()



@app.get("/")
def home():
    return {
        "message": "Weather AI Agent Running"
    }

class ChatRequest(BaseModel):
    message: str
    


@app.post("/chat")
def chat(req: ChatRequest,  authorization: Optional[str] = Header(default=None) ):
    # Load the location cache when the application starts
    current_token.set(authorization)
    
    #store the token in a variable
    answer = ask_agent(req.message)

    return answer
    

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)