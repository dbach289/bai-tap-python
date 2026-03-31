# ===== Bài 3 =====
# Hàm giải phương trình bậc 2
def giai_phuong_trinh_bac_2(a, b, c):
    # Tính delta
    delta = b**2 - 4*a*c
    
    # Kiểm tra delta
    if delta < 0:
        # Phương trình không có nghiệm
        return "Phương trình không có nghiệm"
    elif delta == 0:
        # Phương trình có 1 nghiệm
        x = -b / (2*a)
        return f"Phương trình có 1 nghiệm: x = {x}"
    else:
        # Phương trình có 2 nghiệm
        x1 = (-b + delta**0.5) / (2*a)
        x2 = (-b - delta**0.5) / (2*a)
        return f"Phương trình có 2 nghiệm: x1 = {x1}, x2 = {x2}"

# Ví dụ sử dụng
a = 1  # hệ số a
b = -3  # hệ số b
c = 2  # hệ số c

ket_qua = giai_phuong_trinh_bac_2(a, b, c)
print(ket_qua)