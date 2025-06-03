import os
import json
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

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

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request}
    )

@app.post("/chat")
async def chat_endpoint(
    message: str = Form(...),
    code: str = Form(None),
    history: str = Form(None)
):
    # Convert history from JSON string to list
    message_history = []
    if history:
        try:
            message_history = json.loads(history)
        except:
            pass
    
    # Get response from agent, passing both message and code
    response = get_agent_response(message, code, message_history)
    
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