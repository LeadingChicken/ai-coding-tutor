# Viết code Python của bạn ở đây
def is_palindrome(number):
    # Kiểm tra đầu vào hợp lệ
    if not isinstance(number, int) or number < 0:
        return "Invalid input"
    
    # Chuyển số thành chuỗi
    num_str = str(number)
    
    # So sánh chuỗi gốc với chuỗi đảo ngược
    return num_str == num_str[::-1]

# Nhập và kiểm tra số
try:
    num = int(input("Nhập số nguyên dương: "))
    result = is_palindrome(num)
    if result == True:
        print(f"{num} là số palindrome")
    elif result == False:
        print(f"{num} không phải là số palindrome")
    else:
        print(result)  # In thông báo lỗi
except ValueError:
    print("Invalid input") 