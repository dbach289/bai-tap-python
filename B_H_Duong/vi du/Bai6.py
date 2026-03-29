# ===== Bài 6 =====
# Hàm tính tổng từ 1 đến n
def tinh_tong(n):
    # Sử dụng công thức tính tổng cấp số cộng: n * (n + 1) / 2
    return n * (n + 1) // 2

# Nhập số nguyên dương n
n = int(input("Nhập số nguyên dương n: "))

# Kiểm tra n có phải số nguyên dương
while n <= 0:
    print("Vui lòng nhập số nguyên dương!")
    n = int(input("Nhập số nguyên dương n: "))

# Tính và in tổng từ 1 đến n
tong = tinh_tong(n)
print(f"Tổng từ 1 đến {n} là: {tong}")