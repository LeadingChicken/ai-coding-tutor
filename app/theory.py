from typing import Dict, Any

class ListTheory:
    @staticmethod
    def get_list_theory() -> Dict[str, Any]:
        """
        Returns a comprehensive theory about Python Lists
        """
        return {
            "title": "Python Lists - Comprehensive Guide",
            "sections": [
                {
                    "title": "1. Introduction to Lists",
                    "content": """Lists are one of Python's most fundamental data structures. A list is an ordered, mutable sequence of elements that can store different types of data.

Key characteristics of lists:
• Ordered: Elements maintain their order of insertion
• Mutable: Can be modified after creation
• Dynamic: Can grow or shrink in size
• Heterogeneous: Can contain elements of different types""",
                    "example": """# Creating lists
empty_list = []
numbers = [1, 2, 3, 4, 5]
mixed_list = [1, "hello", 3.14, True]"""
                },
                {
                    "title": "2. List Creation and Access",
                    "content": """Lists can be created in several ways:
• Using square brackets []
• Using the list() constructor
• List comprehension

Elements are accessed using zero-based indexing:
• Positive indices start from 0
• Negative indices start from -1 (last element)""",
                    "example": """# Different ways to create lists
numbers = [1, 2, 3, 4, 5]
converted_list = list("hello")  # ['h', 'e', 'l', 'l', 'o']
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# Accessing elements
first = numbers[0]  # 1
last = numbers[-1]  # 5"""
                },
                {
                    "title": "3. List Slicing",
                    "content": """List slicing allows you to extract portions of a list:
• syntax: list[start:end:step]
• start: starting index (inclusive)
• end: ending index (exclusive)
• step: increment between each item""",
                    "example": """numbers = [0, 1, 2, 3, 4, 5]
first_three = numbers[0:3]  # [0, 1, 2]
every_second = numbers[::2]  # [0, 2, 4]
reversed_list = numbers[::-1]  # [5, 4, 3, 2, 1, 0]"""
                },
                {
                    "title": "4. List Methods",
                    "content": """Common list methods:
• append(): Add element to end
• insert(): Add element at specific position
• extend(): Add elements from another list
• remove(): Remove first occurrence of value
• pop(): Remove and return element at index
• sort(): Sort list in place
• reverse(): Reverse list in place""",
                    "example": """fruits = ['apple']
fruits.append('banana')  # ['apple', 'banana']
fruits.insert(1, 'orange')  # ['apple', 'orange', 'banana']
fruits.extend(['grape', 'kiwi'])  # ['apple', 'orange', 'banana', 'grape', 'kiwi']
fruits.remove('orange')  # ['apple', 'banana', 'grape', 'kiwi']
last = fruits.pop()  # removes and returns 'kiwi'"""
                },
                {
                    "title": "5. List Operations",
                    "content": """Common operations with lists:
• Concatenation (+)
• Repetition (*)
• Membership testing (in)
• Length (len())
• Min and max
• Sum of numeric lists""",
                    "example": """list1 = [1, 2]
list2 = [3, 4]
combined = list1 + list2  # [1, 2, 3, 4]
repeated = list1 * 2  # [1, 2, 1, 2]
exists = 2 in list1  # True
length = len(combined)  # 4
minimum = min(combined)  # 1
total = sum(combined)  # 10"""
                },
                {
                    "title": "6. List Comprehensions",
                    "content": """List comprehensions provide a concise way to create lists:
• Basic syntax: [expression for item in iterable]
• With condition: [expression for item in iterable if condition]
• Nested: [expression for x in iterable1 for y in iterable2]""",
                    "example": """# Basic list comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# With condition
even_squares = [x**2 for x in range(5) if x % 2 == 0]  # [0, 4, 16]

# Nested comprehension
matrix = [[i+j for j in range(3)] for i in range(3)]
# [[0,1,2], [1,2,3], [2,3,4]]"""
                }
            ],
            "practice_questions": [
                {
                    "question": "What will be the output of: [1, 2, 3] + [4, 5]?",
                    "answer": "[1, 2, 3, 4, 5]",
                    "explanation": "The + operator concatenates two lists."
                },
                {
                    "question": "How do you access the last element of a list named 'numbers'?",
                    "answer": "numbers[-1]",
                    "explanation": "Negative indexing starts from the end, with -1 referring to the last element."
                },
                {
                    "question": "What method would you use to add an element to the end of a list?",
                    "answer": "append()",
                    "explanation": "The append() method adds a single element to the end of a list."
                }
            ]
        } 