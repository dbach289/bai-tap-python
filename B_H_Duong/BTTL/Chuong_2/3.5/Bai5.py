# ===== Bài 5 =====
# Nhập các hệ số từ bàn phím
a = float(input("Nhập hệ số a: "))
b = float(input("Nhập hệ số b: "))
c = float(input("Nhập hệ số c: "))

# Tính định thức
d = b**2 - 4*a*c  # Định thức

# Kiểm tra định thức
if d < 0:
    print("Phương trình không có nghiệm thực.")
elif d == 0:
    # Tính nghiệm
    x = -b / (2*a)  # Nghiệm duy nhất
    print(f"Phương trình có nghiệm duy nhất: x = {x}")
else:
    # Tính nghiệm
    import math  # Nhập thư viện math
    x1 = (-b + math.sqrt(d)) / (2*a)  # Nghiệm thứ nhất
    x2 = (-b - math.sqrt(d)) / (2*a)  # Nghiệm thứ hai
    print(f"Phương trình có hai nghiệm: x1 = {x1}, x2 = {x2}")