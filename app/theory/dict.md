# 🐍 BÀI GIẢNG PYTHON: TỪ ĐIỂN (DICTIONARY)

## 1. Dictionary là gì?

- **Dictionary (dict)** là **kiểu dữ liệu lưu trữ theo cặp key-value** (khóa - giá trị).
- Mỗi khóa (key) là duy nhất và dùng để truy cập giá trị tương ứng.

### 📌 Cú pháp:

```python
my_dict = {
    "ten": "Nam",
    "tuoi": 21,
    "nghe": "Sinh viên"
}
```

## 2. Truy cập và thay đổi giá trị

```python
print(my_dict["ten"])      # Nam
my_dict["tuoi"] = 22       # Cập nhật giá trị
```

- Dùng `.get()` để tránh lỗi nếu key không tồn tại:

```python
print(my_dict.get("lop", "Không có thông tin"))  # Không có thông tin
```

## 3. Thêm và xóa phần tử

```python
my_dict["lop"] = "12A1"     # Thêm phần tử mới
del my_dict["nghe"]         # Xóa theo key
value = my_dict.pop("tuoi") # Xóa và trả về giá trị
my_dict.clear()             # Xóa toàn bộ từ điển
```

## 4. Duyệt qua dict

```python
for key in my_dict:
    print(key, my_dict[key])

for key, value in my_dict.items():
    print(f"{key} → {value}")
```

## 5. Một số phương thức hữu ích

```python
keys = my_dict.keys()        # Trả về danh sách các key
values = my_dict.values()    # Trả về danh sách các giá trị
items = my_dict.items()      # Trả về danh sách (key, value)
```

## 6. Dictionary lồng nhau (Nested Dict)

```python
students = {
    "001": {"ten": "Nam", "tuoi": 21},
    "002": {"ten": "Lan", "tuoi": 20}
}

print(students["001"]["ten"])  # Nam
```

## ✅ TÓM TẮT

| Phép Toán         | Mô tả                          | Ví dụ                       |
| ----------------- | ------------------------------ | --------------------------- |
| `dict[key]`       | Truy cập giá trị theo khóa     | `d["ten"]`                  |
| `dict.get(key)`   | Truy cập an toàn               | `d.get("tuoi", "Không có")` |
| `dict[key] = val` | Thêm/Cập nhật giá trị theo key | `d["lop"] = "12A1"`         |
| `del dict[key]`   | Xóa phần tử theo key           | `del d["tuoi"]`             |
| `dict.pop(key)`   | Xóa và trả về giá trị          | `d.pop("tuoi")`             |
| `dict.clear()`    | Xóa tất cả phần tử             | `d.clear()`                 |
| `dict.keys()`     | Trả về danh sách các key       | `d.keys()`                  |
| `dict.values()`   | Trả về danh sách các giá trị   | `d.values()`                |
| `dict.items()`    | Trả về danh sách (key, value)  | `d.items()`                 |
