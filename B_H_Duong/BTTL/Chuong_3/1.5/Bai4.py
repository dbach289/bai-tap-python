# ===== Bài 4 =====

# Nhập số nguyên n từ bàn phím (có kiểm tra lỗi)
while True:
    try:
        n = int(input("Nhập số nguyên n: "))
        break
    except:
        print("Nhập sai, nhập lại!")

# Khởi tạo biến
tong = 0
i = 0

# Duyệt bằng while
while i < n:
    if i % 2 == 0:
        tong += i
    i += 1

# In kết quả
print("Tổng của các số chẵn nhỏ hơn", n, "là:", tong)