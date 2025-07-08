# 🐍 BÀI GIẢNG PYTHON: TẬP HỢP (SET)

## 1. Set là gì?

- **Set** là một **tập hợp không có thứ tự** các phần tử **không trùng lặp**.
- Dùng để loại bỏ các giá trị trùng nhau và thực hiện các phép toán tập hợp như giao, hợp, hiệu, ...

### 📌 Cú pháp:

```python
my_set = {1, 2, 3}
empty_set = set()  # KHÔNG dùng {} vì sẽ tạo ra dict
```

## 2. Đặc điểm của set

- Không có thứ tự ⇒ không thể truy cập bằng chỉ số.
- Không chứa phần tử trùng lặp.

```python
a = {1, 2, 3, 3, 2}
print(a)  # {1, 2, 3}
```

## 3. Các thao tác với set

### ✅ Thêm phần tử

```python
a = {1, 2}
a.add(3)
print(a)  # {1, 2, 3}
```

### ✅ Xóa phần tử

```python
a.remove(2)   # Xóa 2, nếu không có sẽ lỗi
a.discard(5)  # Xóa 5, nếu không có thì KHÔNG lỗi
a.clear()     # Xóa tất cả phần tử
```

## 4. Các phép toán tập hợp

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)   # Hợp: {1, 2, 3, 4, 5}
print(a & b)   # Giao: {3}
print(a - b)   # Hiệu: {1, 2}
print(a ^ b)   # Hiệu đối xứng: {1, 2, 4, 5}
```

## 5. Duyệt qua set

```python
for item in a:
    print(item)
```

## 6. Kiểm tra phần tử

```python
if 3 in a:
    print("Có 3 trong tập hợp")
```

## 7. Chuyển đổi giữa list và set

```python
lst = [1, 2, 2, 3]
s = set(lst)  # Loại bỏ phần tử trùng
print(list(s))  # Chuyển lại thành list
```

## ✅ TÓM TẮT

| Phép Toán    | Mô tả                           | Ví dụ          |
| ------------ | ------------------------------- | -------------- |
| `add(x)`     | Thêm phần tử `x`                | `s.add(4)`     |
| `remove(x)`  | Xóa `x`, lỗi nếu không có       | `s.remove(2)`  |
| `discard(x)` | Xóa `x`, không lỗi nếu không có | `s.discard(5)` |
| `clear()`    | Xóa tất cả phần tử              | `s.clear()`    |
| `&`          | Giao                            | `a & b`        |
| `-`          | Hiệu                            | `a - b`        |
| `^`          | Hiệu đối xứng                   | `a ^ b`        |
