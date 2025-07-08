import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import httpx
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from .config import settings

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# Nếu bạn đã cài anthropic SDK, hãy import và dùng như sau:
# from anthropic import Anthropic, AsyncAnthropic
# anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

# Prompt template cho lý thuyết
THEORY_CHAT_PROMPT_TEMPLATE = """Bạn là AI trợ giảng Python.
Bạn chỉ trả lời các câu hỏi liên quan đến phần lý thuyết Python mà học viên đang học. Hãy hiện câu trả lời dưới dạng markdown.

Lý thuyết đã học:
{theory_context}

Lịch sử trò chuyện:
{chat_history}

Câu hỏi mới nhất: {input}
"""

theory_chat_prompt = PromptTemplate(
    template=THEORY_CHAT_PROMPT_TEMPLATE,
    input_variables=["input", "chat_history", "theory_context"]
)

llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20241022",
    anthropic_api_key=settings.ANTHROPIC_API_KEY,
    temperature=settings.ANTHROPIC_TEMPERATURE,
    max_tokens=4096
)

def format_chat_history(history: List[Dict[str, Any]]) -> str:
    if not history:
        return "Chưa có lịch sử trò chuyện."
    formatted = []
    for msg in history:
        role = "Học viên" if msg.get("role") == "user" else "Tutor"
        formatted.append(f"{role}: {msg.get('content', '')}")
    return "\n".join(formatted)

async def get_theory_chat_response(message: str, history: List[Dict[str, Any]], theory_context: str) -> str:
    chat_history_str = format_chat_history(history)
    prompt = theory_chat_prompt.format(
        input=message,
        chat_history=chat_history_str,
        theory_context=theory_context
    )
    # Gọi LLM (Claude)
    response = await llm.ainvoke(prompt)
    return response.content if hasattr(response, "content") else str(response)