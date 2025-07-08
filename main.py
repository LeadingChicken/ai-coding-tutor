import os
import json
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional, Dict
from fastapi.middleware.cors import CORSMiddleware

from app.models import Message, CodeRequest
from app.agent import get_agent_response
from app.code_executor import run_python_code
from app.generate_exercise import generate_exercise, extract_description, extract_example, extract_explanation, extract_function, extract_unit_test, extract_example_output
from app.theory import ListTheory
from app.theory_chat import get_theory_chat_response

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server address
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    code: Optional[str] = None
    history: Optional[List[dict]] = None
    terminal_output: Optional[str] = None
    exercise: Optional[Dict[str, str]] = None
    is_code_evaluation: Optional[bool] = False

class TheoryChatRequest(BaseModel):
    message: str
    history: List[Dict]
    theory_context: str

class ExerciseRequest(BaseModel):
    topic: str

def run_unit_tests(code: str, unit_test: str) -> str:
    # Kết hợp code của học viên với unit test
    full_code = f"{code}\n\n{unit_test}"
    
    # Thêm imports cần thiết
    imports = """import unittest
import io
import sys
from unittest import TextTestRunner, TestResult
"""
    
    # Thêm custom test runner để capture kết quả chi tiết
    custom_runner_code = """
class CustomTestResult(TestResult):
    def __init__(self):
        super().__init__()
        self.output = []

    def startTest(self, test):
        super().startTest(test)
        
    def addSuccess(self, test):
        super().addSuccess(test)
        test_name = test.id().split('.')[-1]
        self.output.append(f"✅ Test {test_name} passed!")

    def addError(self, test, err):
        super().addError(test, err)
        test_name = test.id().split('.')[-1]
        error_message = str(err[1])
        self.output.append(f"❌ Test {test_name} failed with error: {error_message}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        test_name = test.id().split('.')[-1]
        error_message = str(err[1])
        self.output.append(f"❌ Test {test_name} failed: {error_message}")

class CustomTestRunner(TextTestRunner):
    def _makeResult(self):
        return CustomTestResult()

    def run(self, test):
        result = self._makeResult()
        test(result)
        
        # Tổng hợp kết quả
        output = []
        if result.wasSuccessful():
            output.append("✅ Tất cả unit test đã pass!")
            output.append(f"Số lượng test đã pass: {result.testsRun}")
        else:
            output.append("❌ Một số unit test đã fail!")
            output.append(f"Số lượng test đã chạy: {result.testsRun}")
            output.append(f"Số lượng test fail: {len(result.failures) + len(result.errors)}")
        
        # Thêm kết quả chi tiết từng test
        output.extend(result.output)
        
        return '\\n'.join(output)
"""
    
    # Thêm code để chạy test với custom runner
    run_tests_code = """
# Get test class name dynamically
import re
test_class_match = re.search(r'class\s+(\w+)\s*\(unittest\.TestCase\)', __unit_test__)
if not test_class_match:
    raise ValueError("Could not find test class in unit test code")

test_class_name = test_class_match.group(1)

# Get all test cases using the found class name
suite = unittest.TestLoader().loadTestsFromTestCase(eval(test_class_name))

# Run tests with custom runner
runner = CustomTestRunner(stream=None)
result = runner.run(suite)
print(result)  # In kết quả test
"""

    # Kết hợp tất cả code và tạo namespace
    full_code = imports + full_code + "\n\n" + custom_runner_code + "\n" + run_tests_code
    
    # Tạo namespace với unit_test code
    namespace = {'__unit_test__': unit_test}
    
    # Chạy code với namespace đã được cung cấp
    return run_python_code(full_code, namespace)

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request}
    )

@app.get("/theory", response_class=HTMLResponse)
async def theory_page(request: Request):
    return templates.TemplateResponse(
        "theory.html",
        {"request": request}
    )

@app.post("/generate_exercise")
async def generate_exercise_endpoint(request: ExerciseRequest):
    """Generate a new Python exercise."""
    print(request.topic)
    content = generate_exercise(request.topic)
    
    print(extract_unit_test(content))
    return {
        "description": extract_description(content),
        "example": extract_example(content),
        "example_output": extract_example_output(content),
        "explanation": extract_explanation(content),
        "function": extract_function(content),
        "unit_test": extract_unit_test(content)
    }

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Get response from agent, passing message, code, and terminal output
    response = get_agent_response(
        message=request.message,
        code=request.code,
        history=request.history or [],
        terminal_output=request.terminal_output,
        exercise=request.exercise,
        is_code_evaluation=request.is_code_evaluation
    )
    
    return {
        "response": response
    }

@app.post("/run_code")
async def run_code_endpoint(request: CodeRequest):
    """Execute Python code and return the output."""
    output = run_python_code(request.code)
    return {"output": output}

@app.post("/run_unit_tests")
async def run_unit_tests_endpoint(request: CodeRequest):
    """Run unit tests on the submitted code without LLM evaluation."""
    if not request.code or not request.unit_test:
        raise HTTPException(status_code=400, detail="Missing code or unit test")
    
    # Chạy unit test
    test_output = run_unit_tests(request.code, request.unit_test)
    return {
        "test_output": test_output
    }

@app.post("/test_code")
async def test_code_endpoint(request: ChatRequest):
    """Run unit tests and get AI evaluation."""
    if not request.code or not request.exercise or not request.exercise.get("unit_test"):
        raise HTTPException(status_code=400, detail="Missing code or unit test")
    
    # Chạy unit test
    test_output = run_unit_tests(request.code, request.exercise["unit_test"])
    
    # Gửi kết quả cho agent để đánh giá
    agent_response = get_agent_response(
        message="Hãy đánh giá kết quả unit test của học viên",
        code=request.code,
        terminal_output=test_output,
        exercise=request.exercise,
        is_code_evaluation=True
    )
    
    return {
        "test_output": test_output,
        "agent_response": agent_response
    }

@app.get("/api/theory/{lesson_id}")
async def get_theory(lesson_id: str):
    """Get theory content for a specific lesson."""
    theory_dir = os.path.join(os.path.dirname(__file__), "app", "theory")
    theory_file = os.path.join(theory_dir, f"{lesson_id}.md")
    
    if not os.path.exists(theory_file):
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    try:
        with open(theory_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse markdown content into sections
        sections = []
        current_title = None
        current_content = []
        
        for line in content.split('\n'):
            # Only process level 2 headings (##)
            if line.startswith('## '):
                # Save previous section if exists
                if current_title is not None:
                    sections.append({
                        "title": current_title,
                        "content": '\n'.join(current_content).strip()
                    })
                # Start new section
                current_title = line[3:].strip()
                current_content = []
            else:
                # Add line to current content
                current_content.append(line)
        
        # Add the last section
        if current_title is not None:
            sections.append({
                "title": current_title,
                "content": '\n'.join(current_content).strip()
            })
        
        return {"content": sections}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/theory_chat")
async def theory_chat_endpoint(request: TheoryChatRequest):
    response = await get_theory_chat_response(
        message=request.message,
        history=request.history,
        theory_context=request.theory_context
    )
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)