import random
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def get_context():
    """Return 2 random context from the list of available contexts."""
    contexts = ["leo núi", "câu cá", "mối quan hệ", "bóng đá", "âm nhạc", "sách", "nấu ăn"]
    return random.sample(contexts, 2)

def generate_exercise(topic):
    """Generate a Python exercise using GPT-4 based on random topic and context."""
    context = get_context()
    print(topic, context)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create prompt for GPT-4
    prompt = f"""
    Mô tả: Viết một hàm `fish_stats(fish_counts: List[int]) -> List[int]` nhận vào danh sách `fish_counts`, trong đó mỗi phần tử đại diện cho số cá câu được trong một lần ra hồ. Hàm cần trả về một danh sách gồm:
    - Tổng số lần câu cá.
    - Tổng số cá đã câu được.
    - Số lần không câu được con cá nào (gi  á trị = 0).
    - Số lần câu được trên 5 con cá.
    Ví dụ:
    ```python
    fish_counts = [1, 2, 3, 4, 5, 0, 0, 0, 0, 0]
    fish_stats(fish_counts)
    ```
    Output:
    ```python
    [15, 15, 5, 1]
    ```
    Giải thích: 
    - Tổng số lần câu cá: 1 + 2 + 3 + 4 + 5 + 0 + 0 + 0 + 0 + 0 = 15
    - Tổng số cá đã câu được: 1 + 2 + 3 + 4 + 5 = 15
    - Số lần không câu được con cá nào: 5
    - Số lần câu được trên 5 con cá: 1

    Hàm cần hoàn chỉnh:
    ```python
    from typing import List
    def fish_stats(fish_counts: List[int]) -> List[int]:
        # fish_counts: danh sách số lượng cá câu được trong mỗi lần ra hồ
        # return: danh sách gồm 4 phần tử:
        #   - Tổng số lần câu cá
        #   - Tổng số cá đã câu được
        #   - Số lần không câu được con cá nào
        #   - Số lần câu được trên 5 con cá

        # TODO: Hoàn thành hàm
        pass
    ```

    Unit test:
    ```python
    import unittest
    class TestFishStats(unittest.TestCase):
        def test_fish_stats(self):
            self.assertEqual(fish_stats([1, 2, 3, 4, 5, 0, 0, 0, 0, 0]), [15, 15, 5, 1])
            self.assertEqual(fish_stats([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), [0, 0, 10, 0])
            self.assertEqual(fish_stats([10, 10, 10, 10, 10, 10, 10, 10, 10, 10]), [100, 100, 0, 10])
    ```
    
    ----------------------------
    Hãy tạo một bài tập Python giống ví dụ trên về chủ đề {topic} với ngữ cảnh về {context[0]} và {context[1]}.
    Bài tập phải có format như sau:
    - Mô tả:
    - Ví dụ:
    - Giải thích:
    - Hàm cần hoàn chỉnh:
    - Unit test:
    
    Hãy viết bằng tiếng Việt và đảm bảo bài tập có độ khó trung bình, phù hợp với người học Python. Nếu bạn đưa ra code ví dụ thì hãy viết bằng tiếng anh. Hãy tuân thủ format và đừng thêm bất kỳ thông tin nào khác."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là một giáo viên dạy lập trình Python chuyên nghiệp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Có lỗi khi tạo bài tập: {str(e)}"
    
def extract_description(content):
    """Extract the description from the content."""
    return content.split("- Mô tả:")[1].split("- Ví dụ:")[0].strip()

def normalize_code_block(text):
    """Helper function to normalize code blocks by removing extra indentation and markdown syntax."""
    # Split into lines
    lines = text.split('\n')
    
    # Remove markdown code block syntax
    if lines[0].strip() == "```python":
        lines = lines[1:]
    if lines[-1].strip() == "```":
        lines = lines[:-1]
    
    # Process indentation
    processed_lines = []
    min_indent = float('inf')
    non_empty_lines = [line for line in lines if line.strip()]
    
    # First pass: find minimum indentation
    for line in non_empty_lines:
        indent = len(line) - len(line.lstrip())
        if indent < min_indent:
            min_indent = indent
    
    # Second pass: normalize indentation
    for line in lines:
        if line.strip():  # If line is not empty
            current_indent = len(line) - len(line.lstrip())
            if current_indent >= min_indent:
                line = line[min_indent:]
        processed_lines.append(line)
    
    # Join the lines back together
    return '\n'.join(processed_lines).strip()

def extract_function(content):
    """Extract the function from the content and remove markdown formatting."""
    function_block = content.split("- Hàm cần hoàn chỉnh:")[1].split("- Unit test:")[0].strip()
    return normalize_code_block(function_block)

def extract_example(content):
    """Extract the example from the content and normalize formatting."""
    example_block = content.split("- Ví dụ:")[1].split("- Giải thích:")[0].strip()
    
    # Split into input and output sections if they exist
    sections = example_block.split("Output:")
    
    if len(sections) > 1:
        # Process input section
        input_section = sections[0].strip()
        return input_section
    else:
        # If there's no explicit Output section, return the entire block
        return example_block.strip()

def extract_example_output(content):
    """Generate the example output from the content."""
    example_block = content.split("- Ví dụ:")[1].split("- Giải thích:")[0].strip()
    sections = example_block.split("Output:")
    
    if len(sections) > 1:
        output_section = sections[1].strip()
        return output_section
    return ""

def extract_explanation(content):
    """Extract the explanation from the content."""
    return content.split("- Giải thích:")[1].split("- Hàm cần hoàn chỉnh:")[0].strip()

def extract_unit_test(content):
    """Extract the unit test from the content and remove markdown formatting."""
    test_block = content.split("- Unit test:")[1].strip()
    return normalize_code_block(test_block)
