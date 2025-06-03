from typing import List, Dict, Any, Union
from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from .config import settings
import json

# Define the tools
def read_code(code_from_sandbox: str = "") -> str:
    """Read code from the sandbox editor."""
    try:
        if not code_from_sandbox or code_from_sandbox.strip() == "":
            return "# Không có code nào trong sandbox để đọc."
        return code_from_sandbox.strip()
    except Exception as e:
        return f"Lỗi khi đọc code: {str(e)}"

def write_code(input_data: Union[str, Dict[str, str]]) -> str:
    """Write code to a file."""
    try:
        # Convert string input to dictionary if needed
        if isinstance(input_data, str):
            try:
                input_dict = json.loads(input_data)
            except json.JSONDecodeError:
                return "Error: Input must be a valid JSON string or dictionary"
        else:
            input_dict = input_data
            
        # Extract file_path and content
        file_path = input_dict.get('file_path')
        content = input_dict.get('content')
        
        if not file_path or not content:
            return "Error: Both file_path and content are required in the input"
            
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Successfully wrote code to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# Define the tools list
tools = [
    Tool(
        name="read_code",
        func=read_code,
        description="Sử dụng tool này khi bạn cần đọc code từ sandbox"
    ),
    # Tool(
    #     name="write_code",
    #     func=write_code,
    #     description="Use this tool when you need to write or update code in a file. Input should be a dictionary with 'file_path' and 'content' keys in JSON format."
    # )
]

# Define the agent's prompt template
AGENT_PROMPT = """Bạn là một AI tutor chuyên nghiệp về lập trình. Nhiệm vụ của bạn là giúp học viên học lập trình và giải quyết các vấn đề code.

Bạn có quyền truy cập vào các công cụ sau:
{tools}

Các công cụ có sẵn: {tool_names}

Khi phân tích và đưa ra quyết định, hãy:
1. Đọc và hiểu yêu cầu của học viên
2. Xem xét ngữ cảnh của cuộc trò chuyện
3. Nếu học viên yêu cầu review code, giải thích hoặc chỉnh sửa code, hãy sử dụng read_code để đọc code từ sandbox
4. Sau khi đọc code, hãy phân tích và giải thích code một cách chi tiết
5. KHÔNG sử dụng read_code nhiều lần trong cùng một câu trả lời
6. Nếu bạn không hiểu ý của học viên, hãy hỏi lại chứ đừng cố gắng đưa ra câu trả lời

Ví dụ về cách sử dụng read_code:
Question: Hãy giải thích code của tôi
Thought: Tôi sẽ đọc code từ sandbox để phân tích và giải thích
Action: read_code
Action Input: ""
Observation: def example():
    print("Hello World")
Final Answer: Đoạn code trên định nghĩa một hàm tên là `example` có chức năng in ra chuỗi "Hello World" khi được gọi...

Sử dụng định dạng sau để trả lời (PHẢI tuân thủ chính xác thứ tự này):
Question: <câu hỏi của học viên>
Thought: <suy nghĩ về cách giải quyết vấn đề>
Action: read_code
Action Input: ""
Observation: <kết quả từ công cụ>
Final Answer: <phân tích và giải thích code>

Hãy trả lời bằng tiếng Việt và luôn giải thích chi tiết lý do đằng sau mỗi quyết định.
Lưu ý: Tuyệt đối KHÔNG được gọi read_code nhiều hơn 1 lần trong một câu hỏi. Nếu đã có Observation từ read_code, hãy tiếp tục phân tích thay vì gọi lại.
Question: {input}
{agent_scratchpad}"""

# Create the agent
prompt = PromptTemplate(
    template=AGENT_PROMPT,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
)

def format_chat_history(history: List[Dict[str, Any]]) -> str:
    """Format chat history for the prompt."""
    if not history:
        return "Chưa có lịch sử trò chuyện."
    
    formatted_history = []
    for msg in history:
        role = "Học viên" if msg.get("role") == "user" else "Tutor"
        content = msg.get("content", "")
        formatted_history.append(f"{role}: {content}")
    
    return "\n".join(formatted_history)

def get_agent_response(message: str, code: str = None, history: List[Dict[str, Any]] = None) -> str:
    """Get response from the agent."""
    try:
        # Format chat history
        chat_history = format_chat_history(history or [])
        
        # Combine history and current message
        full_message = f"""Lịch sử trò chuyện:
{chat_history}

Câu hỏi hiện tại: {message}"""

        # Create a new executor with the code from sandbox
        agent_executor = AgentExecutor(
            agent=agent,
            tools=[Tool(
                name="read_code",
                func=lambda _: code.strip() if code else "# Không có code nào trong sandbox để đọc.",
                description="Sử dụng tool này khi bạn cần đọc code từ sandbox"
            )],
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
            
        response = agent_executor.invoke({"input": full_message})
        return response["output"]
    except Exception as e:
        return f"Xin lỗi, đã có lỗi xảy ra: {str(e)}\nVui lòng thử lại với câu hỏi khác hoặc điều chỉnh lại yêu cầu của bạn."

# Create the agent
llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    temperature=settings.OPENAI_TEMPERATURE,
    openai_api_key=settings.OPENAI_API_KEY
)

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=20  # Limit maximum iterations to prevent infinite loops
) 