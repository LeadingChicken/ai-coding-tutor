from typing import List, Dict, Any
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.callbacks import StdOutCallbackHandler
from .config import settings

# Biến lưu trữ bài tập hiện tại
current_exercise = {
    "description": "",
    "example": "",
    "example_output": "",
    "explanation": "",
    "function": "",
    "unit_test": ""
}

# Tạo LLM
llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20241022",
    anthropic_api_key=settings.ANTHROPIC_API_KEY,
    temperature=settings.ANTHROPIC_TEMPERATURE,
    max_tokens=4096
)

# Prompt template cho chat thông thường
CHAT_PROMPT_TEMPLATE = """Bạn là một AI tutor chuyên nghiệp về lập trình.
Nhiệm vụ của bạn là giúp học viên học lập trình và giải quyết các vấn đề code. Bạn đang hướng dẫn một học viên làm bài tập của họ nên hãy giữ tôn trọng học viên và hướng dẫn họ một cách tốt nhất.

Bạn có quyền truy cập vào các công cụ sau:
{tools}

Các công cụ có sẵn: {tool_names}

Lịch sử trò chuyện:
{chat_history}

Bài tập hiện tại:
Mô tả: {description}
Ví dụ:
{example}
Output:
{example_output}
Giải thích: {explanation}
Hàm cần hoàn chỉnh:
{function}
Unit test:
{unit_test}

Khi phân tích và đưa ra quyết định, hãy:
1. Đọc và hiểu yêu cầu của học viên.
2. Xem xét ngữ cảnh từ lịch sử trò chuyện nếu có.
3. Nếu học viên yêu cầu review, giải thích hoặc chỉnh sửa code của họ, hãy dùng read_code để đọc code từ sandbox.
4. Nếu học viên hỏi về bài tập hiện tại:
   - Giải thích yêu cầu bài tập một cách rõ ràng
   - Cung cấp gợi ý phù hợp nếu học viên cần
   - Kiểm tra code của học viên và đưa ra nhận xét
5. Đừng bao giờ đưa code cho học viên, thay vào đó nếu học viên có hỏi về cách làm bài hãy cố gắng đưa ra những gợi ý mà bạn nghĩ là tốt nhất.
6. LUÔN LUÔN tuân theo định dạng sau một cách chính xác:

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

# Prompt template cho đánh giá code
CODE_EVALUATION_PROMPT_TEMPLATE = """Bạn là một AI tutor chuyên nghiệp về lập trình.
Nhiệm vụ của bạn là đánh giá code của học viên và đưa ra nhận xét phù hợp. Hãy giữ thái độ tích cực và khuyến khích học viên.

Bạn có quyền truy cập vào các công cụ sau:
{tools}

Các công cụ có sẵn: {tool_names}

Lịch sử trò chuyện:
{chat_history}

Bài tập hiện tại:
Mô tả: {description}
Ví dụ:
{example}
Output:
{example_output}
Giải thích: {explanation}
Hàm cần hoàn chỉnh:
{function}
Unit test:
{unit_test}

Khi đánh giá code của học viên, hãy:
1. Đọc code của học viên bằng công cụ read_code
2. Đọc terminal output bằng công cụ read_terminal_output
3. So sánh kết quả với yêu cầu bài tập
4. Đưa ra nhận xét:
   - Nếu code chạy đúng:
     + Khen ngợi học viên một cách cụ thể (ví dụ: cách giải quyết hay, code sạch, v.v.)
     + Đề xuất cách tối ưu hóa nếu có
     + Khuyến khích học viên tiếp tục phát triển
   - Nếu code chưa đúng:
     + Chỉ ra vấn đề một cách rõ ràng nhưng nhẹ nhàng
     + Đưa ra gợi ý để học viên tự sửa (KHÔNG đưa đáp án)
     + Động viên học viên cố gắng
5. LUÔN LUÔN tuân theo định dạng sau một cách chính xác:

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

# Prompt objects
chat_prompt = PromptTemplate(
    template=CHAT_PROMPT_TEMPLATE,
    input_variables=["input", "tools", "tool_names", "agent_scratchpad", "chat_history", 
                    "description", "example", "example_output", "explanation", "function", "unit_test"]
)

code_evaluation_prompt = PromptTemplate(
    template=CODE_EVALUATION_PROMPT_TEMPLATE,
    input_variables=["input", "tools", "tool_names", "agent_scratchpad", "chat_history", 
                    "description", "example", "example_output", "explanation", "function", "unit_test"]
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

def get_agent_response(message: str, code: str = None, history: List[Dict[str, Any]] = None, terminal_output: str = None, exercise: Dict[str, str] = None, is_code_evaluation: bool = False) -> str:
    try:
        # Format history nếu có
        chat_history_str = format_chat_history(history) if history else "Chưa có lịch sử trò chuyện."

        # Cập nhật current_exercise nếu có
        global current_exercise
        if exercise:
            current_exercise.update(exercise)

        # Closure để giữ biến code và terminal_output
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

        # Chọn prompt phù hợp
        prompt = code_evaluation_prompt if is_code_evaluation else chat_prompt

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
            "description": current_exercise["description"],
            "example": current_exercise["example"],
            "example_output": current_exercise["example_output"],
            "explanation": current_exercise["explanation"],
            "function": current_exercise["function"],
            "unit_test": current_exercise["unit_test"],
            "agent_scratchpad": ""
        })

        # Thêm metadata cho code blocks
        output = response["output"]
        return output

    except Exception as e:
        return f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"
