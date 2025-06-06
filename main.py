import os
import json
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

from app.models import Message, CodeRequest
from app.agent import get_agent_response
from app.code_executor import run_python_code

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    code: Optional[str] = None
    history: Optional[List[dict]] = None
    terminal_output: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request}
    )

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Get response from agent, passing message, code, and terminal output
    response = get_agent_response(
        message=request.message,
        code=request.code,
        history=request.history or [],
        terminal_output=request.terminal_output
    )
    
    return {
        "response": response
    }

@app.post("/run_code")
async def run_code_endpoint(request: CodeRequest):
    """Execute Python code and return the output."""
    output = run_python_code(request.code)
    return {"output": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)