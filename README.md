# AI Coding Tutor

AI Coding Tutor là một ứng dụng web tương tác giúp học viên học lập trình Python thông qua việc trao đổi với một AI tutor thông minh. Dự án sử dụng FastAPI làm backend và tích hợp với OpenAI API để tạo ra trải nghiệm học tập tương tác.

## Tính năng chính

- 💬 Chat tương tác với AI tutor
- 📝 Code editor tích hợp với syntax highlighting
- ▶️ Thực thi code Python trực tiếp trên giao diện
- 🔍 Phân tích và giải thích code chi tiết
- 📚 Lưu trữ lịch sử chat để theo dõi quá trình học tập

## Yêu cầu hệ thống

- Python 3.8+
- Anthropic API key
- OpenAI API key

## Cài đặt

1. Clone repository:

```bash
git clone https://github.com/LeadingChicken/ai-coding-tutor
cd ai-coding-tutor
```

2. Tạo và kích hoạt môi trường ảo:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

4. Tạo file `.env` từ mẫu:

```bash
# Copy file mẫu
cp .env.example .env
# Sau đó chỉnh sửa file .env và thêm API key của bạn
```

File `.env` cần có các biến môi trường sau:

```
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_TEMPERATURE=0.7
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

⚠️ **Lưu ý bảo mật**:

- KHÔNG commit file `.env` lên git
- KHÔNG chia sẻ API key của bạn
- File `.env` đã được thêm vào `.gitignore`

## Khởi chạy ứng dụng

1. Chạy server:

```bash
python main.py
```

2. Truy cập ứng dụng tại: http://localhost:8000

## Cấu trúc project

```bash
ai-coding-tutor/
├── app/
│   ├── agent.py      # AI tutor agent logic
│   ├── models.py     # Pydantic models
│   └── code_executor.py  # Code execution handler
├── static/           # Static files (CSS, JS)
├── templates/        # HTML templates
├── main.py          # FastAPI application
├── .env    # Mẫu file cấu hình, bạn hãy tạo nó
├── .gitignore       # Git ignore rules
└── requirements.txt  # Project dependencies
```

## Công nghệ sử dụng

- **Backend**: FastAPI
- **AI/ML**: OpenAI API, LangChain, Anthropic API
- **Frontend**: HTML, CSS, JavaScript, Vue.js

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request nếu bạn muốn cải thiện dự án.
