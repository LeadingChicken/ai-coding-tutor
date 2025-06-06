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

# Prompt template
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
3. Nếu học viên yêu cầu review, giải thích hoặc chỉnh sửa code của họ, hãy dùng read_code để đọc code từ sandbox.
4. Nếu được học viên yêu cầu gợi ý những bài tập, hãy đưa ra những bài tập mà bạn nghĩ là phù hợp nhất với trình độ của học viên.
5. Nếu bạn được học viên bảo gợi ý cách làm bài tập thì cố gắng đưa ra những gợi ý mà bạn nghĩ là tốt nhất. Đừng đưa họ code mẫu, mà hãy đưa ra những gợi ý mà bạn nghĩ là tốt nhất.
6. Nếu như bạn cần đọc terminal output (ví dụ như bạn cần đọc lỗi hay sửa lỗi cho học viên), hãy sử dụng read_terminal_output.
7. LUÔN LUÔN tuân theo định dạng sau một cách chính xác:

Thought: suy nghĩ về những gì bạn sẽ làm
Action: tên công cụ bạn sẽ sử dụng (nếu cần)
Action Input: input cho công cụ (nếu cần)

HOẶC

Final Answer: câu trả lời cuối cùng (hãy tổng hợp lại toàn bộ câu trả lời của bạn từ đầu bao gồm cả Thought)

LƯU Ý QUAN TRỌNG:
- Nếu bạn cần sử dụng công cụ, PHẢI có cả Action và Action Input
- Nếu không cần sử dụng công cụ, PHẢI kết thúc bằng Final Answer
- KHÔNG được trả lời mà thiếu Thought ở đầu
- KHÔNG được trả lời tự do không theo format
- Khi trả lời có chứa code mẫu, PHẢI đặt code trong block ```python:copyable và kết thúc bằng ```. Ví dụ:
  ```python:copyable
  print("Hello World")
  ```

Câu hỏi: {input}
{agent_scratchpad}"""

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

def get_agent_response(message: str, code: str = None, history: List[Dict[str, Any]] = None, terminal_output: str = None) -> str:
    try:
        # Format history nếu có
        chat_history_str = format_chat_history(history) if history else "Chưa có lịch sử trò chuyện."

        # Tạo closure để giữ biến code và terminal_output
        def read_code_with_input(input_str=None):
            # Bỏ qua input_str, luôn trả về code nếu có
            if code:
                return f"```python\n{code.strip()}\n```"
            return "Không có code nào trong sandbox để đọc."

        def read_terminal_output(input_str=None):
            # Bỏ qua input_str, luôn trả về terminal output nếu có
            if terminal_output:
                return f"Terminal Output:\n```\n{terminal_output.strip()}\n```"
            return "Không có terminal output nào để đọc."

        tools = [
            Tool(
                name="read_code",
                func=read_code_with_input,
                description="Đọc code từ sandbox của học viên. Trả về code dưới dạng markdown Python block."
            ),
            Tool(
                name="read_terminal_output",
                func=read_terminal_output,
                description="Đọc terminal output từ lần chạy code gần nhất của học viên. Trả về output dưới dạng markdown code block."
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

        # Thêm metadata cho code blocks
        output = response["output"]
        return output

    except Exception as e:
        return f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"
