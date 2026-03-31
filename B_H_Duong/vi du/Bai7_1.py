# ===== Bài 7 =====
# Hàm tính tổng ba canh tam giác
def tinh_tong_ba_canh(a, b, c):
    # Kiểm tra xem ba canh có thể tạo thành tam giác hay không
    if a + b > c and a + c > b and b + c > a:
        # Tính tổng ba canh
        tong_ba_canh = a + b + c
        return tong_ba_canh
    else:
        return "Ba canh khong the tao thanh tam giac"

# Hàm tính chu vi tam giác
def tinh_chu_vi(a, b, c):
    # Kiểm tra xem ba canh có thể tạo thành tam giác hay không
    if a + b > c and a + c > b and b + c > a:
        # Tính chu vi
        chu_vi = a + b + c
        return chu_vi
    else:
        return "Ba canh khong the tao thanh tam giac"

# Ví dụ sử dụng
a = 3
b = 4
c = 5

tong_ba_canh = tinh_tong_ba_canh(a, b, c)
chu_vi = tinh_chu_vi(a, b, c)

print(f"Tong ba canh: {tong_ba_canh}")
print(f"Chu vi: {chu_vi}")