import os
from typing import List
import markdown2
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
import re

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .config import settings

# Validate settings on module load
settings.validate()

# System message for the coding tutor
SYSTEM_MESSAGE = """Bạn là một giảng viên lập trình chuyên nghiệp. Nhiệm vụ của bạn là giúp học sinh học lập trình và giải quyết các bài tập code.

Nguyên tắc khi dạy:
- Giải thích khái niệm rõ ràng và đưa ra ví dụ cụ thể
- Chia nhỏ vấn đề phức tạp thành các bước đơn giản
- Khuyến khích viết code sạch và áp dụng best practices
- Chỉ ra các lỗi thường gặp và cách tránh
- Sử dụng code mẫu để minh họa
- Kiên nhẫn trả lời các câu hỏi của học sinh
- Khi học sinh chia sẻ code, phân tích và đưa ra nhận xét
- Đề xuất cách cải thiện code và giải thích lý do

Hãy trả lời bằng tiếng Việt và sử dụng Markdown. Sử dụng code blocks với language tag phù hợp khi đưa ra code mẫu."""

# Initialize chat model
chat = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    temperature=settings.OPENAI_TEMPERATURE,
    openai_api_key=settings.OPENAI_API_KEY
)

def process_code_blocks(content: str) -> str:
    """Process code blocks with syntax highlighting."""
    def replace_code_block(match):
        language = match.group(1) or 'python'  # Default to python if no language specified
        code = match.group(2)
        
        try:
            lexer = get_lexer_by_name(language)
            formatter = HtmlFormatter(style='monokai')
            highlighted = highlight(code, lexer, formatter)
            return highlighted
        except:
            # If language isn't supported, return original code block
            return f'<pre><code class="{language}">{code}</code></pre>'
    
    # Replace ```language\ncode``` blocks
    pattern = r'```(\w+)?\n(.*?)```'
    content = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)
    
    # Convert remaining Markdown to HTML
    content = markdown2.markdown(content)
    return content

def get_chat_response(message: str, code: str = None, history: List[dict] = None) -> str:
    """Get response from the chat model."""
    # Convert history to LangChain message format
    messages = [SystemMessage(content=SYSTEM_MESSAGE)]
    
    if history:
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
    
    # If code is provided, add it to the message
    if code and code.strip():
        message = f"{message}\n\nHere's my code:\n```python\n{code}\n```"
    
    # Add the current message
    messages.append(HumanMessage(content=message))
    
    # Get response from the model
    response = chat(messages)
    
    # Process markdown and code blocks
    return process_code_blocks(response.content) 