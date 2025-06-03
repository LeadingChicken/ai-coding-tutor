from typing import List, Dict, Any
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import StdOutCallbackHandler
from .config import settings

# Tạo LLM
llm = ChatOpenAI(
    model_name=settings.OPENAI_MODEL,
    temperature=settings.OPENAI_TEMPERATURE,
    api_key=settings.OPENAI_API_KEY
)

# Prompt template chuẩn LangChain
AGENT_PROMPT_TEMPLATE = """Bạn là một AI tutor chuyên nghiệp về lập trình.
Nhiệm vụ của bạn là giúp học viên học lập trình và giải quyết các vấn đề code.

Bạn có quyền truy cập vào các công cụ sau:
{tools}

Các công cụ có sẵn: {tool_names}

Lịch sử trò chuyện:
{chat_history}

Khi phân tích và đưa ra quyết định, hãy:
1. Đọc và hiểu yêu cầu của học viên.
2. Xem xét ngữ cảnh từ lịch sử trò chuyện nếu có.
3. Nếu học viên yêu cầu review, giải thích hoặc chỉnh sửa code, hãy dùng read_code để đọc code từ sandbox.
4. KHÔNG gọi read_code nhiều hơn một lần trong một phiên.
5. Luôn tuân theo định dạng:
Thought: ...
Action: ...
Action Input: ...
hoặc
Final Answer: ...

Câu hỏi: {input}
{agent_scratchpad}
"""

# Prompt object
prompt = PromptTemplate(
    template=AGENT_PROMPT_TEMPLATE,
    input_variables=["input", "tools", "tool_names", "agent_scratchpad", "chat_history"]
)

# Hàm format lịch sử trò chuyện (nếu dùng)
def format_chat_history(history: List[Dict[str, Any]]) -> str:
    if not history:
        return "Chưa có lịch sử trò chuyện."
    formatted = []
    for msg in history:
        role = "Học viên" if msg.get("role") == "user" else "Tutor"
        formatted.append(f"{role}: {msg.get('content', '')}")
    return "\n".join(formatted)

def read_code_func(code):
    print(f"[DEBUG] Code nhận được trong tool: {repr(code)}")
    if code and code.strip() != "":
        return code.strip()
    else:
        return "# Không có code nào trong sandbox để đọc."

# Hàm chính
def get_agent_response(message: str, code: str = None, history: List[Dict[str, Any]] = None) -> str:
    try:
        # Format history nếu có
        chat_history_str = format_chat_history(history) if history else "Chưa có lịch sử trò chuyện."

        def read_code_func(_):
            print(f"[DEBUG] Code nhận được trong tool: {repr(code)}")
            if code and code.strip() != "":
                return code.strip()
            else:
                return "# Không có code nào trong sandbox để đọc."

        tools = [
            Tool(
                name="read_code",
                func=read_code_func,
                description="Sử dụng tool này khi bạn cần đọc code từ sandbox của học viên."
            )
        ]

        agent = create_react_agent(
            llm=llm,
            tools=tools,
            prompt=prompt
        )

        executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            return_intermediate_steps=True,
            callbacks=[StdOutCallbackHandler()]
        )

        # Gửi input và các thông tin cần thiết
        response = executor.invoke({
            "input": message,
            "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
            "tool_names": [tool.name for tool in tools],
            "chat_history": chat_history_str,
            "agent_scratchpad": ""
        })

        return response["output"]

    except Exception as e:
        return f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"
