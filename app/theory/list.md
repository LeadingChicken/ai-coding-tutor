# 🐍 BÀI GIẢNG PYTHON: DANH SÁCH (LIST)

## 1. Danh sách (List) là gì?

- **Danh sách (List)** trong Python là một **kiểu dữ liệu có thể chứa nhiều giá trị** (phần tử), được **lưu trữ theo thứ tự**.
- Một danh sách có thể chứa các **kiểu dữ liệu khác nhau** như số, chuỗi, thậm chí cả danh sách khác.

### 📌 Cú pháp:

```python
ten_list = [gia_tri_1, gia_tri_2, gia_tri_3, ...]
```

### 📌 Ví dụ:

```python
fruits = ["táo", "cam", "chuối"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hai", 3.0, True]
```

## 2. Truy cập phần tử trong list

- Dùng **chỉ số (index)** bắt đầu từ **0**:

```python
fruits = ["táo", "cam", "chuối"]
print(fruits[0])  # táo
print(fruits[2])  # chuối
```

- **Chỉ số âm** để truy cập từ cuối danh sách:

```python
print(fruits[-1])  # chuối
print(fruits[-2])  # cam
```

## 3. Duyệt qua danh sách

```python
for fruit in fruits:
    print(fruit)
```

## 4. Một số thao tác với list

### ✅ Thêm phần tử

```python
fruits.append("xoài")      # thêm vào cuối danh sách
fruits.insert(1, "ổi")     # chèn "ổi" vào vị trí thứ 1
```

### ✅ Xóa phần tử

```python
fruits.remove("cam")       # xóa theo giá trị
del fruits[0]              # xóa theo chỉ số
x = fruits.pop()           # xóa và trả về phần tử cuối cùng
```

### ✅ Độ dài danh sách

```python
print(len(fruits))
```

### ✅ Cắt danh sách (slicing)

```python
print(fruits[1:3])  # từ vị trí 1 đến vị trí 2
```

### ✅ Kiểm tra tồn tại

```python
if "chuối" in fruits:
    print("Có chuối!")
```

## 5. Một số hàm và phương thức hữu ích

```python
numbers = [3, 1, 4, 2]

numbers.sort()     # Sắp xếp tăng dần
numbers.reverse()  # Đảo ngược danh sách
print(min(numbers))  # Phần tử nhỏ nhất
print(max(numbers))  # Phần tử lớn nhất
print(sum(numbers))  # Tổng các phần tử
```

## 6. List lồng nhau (Nested List)

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

print(matrix[0][1])  # 2
```

## 7. Ví dụ thực hành

✅ Tạo một danh sách các số nguyên từ 1 đến 5, nhân đôi từng số và in ra kết quả:

```python
numbers = [1, 2, 3, 4, 5]

for n in numbers:
    print(n * 2)
```

## ✅ TÓM TẮT

| Phép Toán  | Mô tả                      | Ví dụ                   |
| ---------- | -------------------------- | ----------------------- |
| `append()` | Thêm phần tử vào cuối      | `my_list.append(5)`     |
| `insert()` | Chèn phần tử vào vị trí    | `my_list.insert(1, 10)` |
| `remove()` | Xóa phần tử theo giá trị   | `my_list.remove(2)`     |
| `pop()`    | Xóa và trả về phần tử cuối | `my_list.pop()`         |
| `len()`    | Độ dài danh sách           | `len(my_list)`          |
| `in`       | Kiểm tra tồn tại           | `if 3 in my_list:`      |
