# ===== Bài 4 =====
# Nhập số nguyên n từ bàn phím
n = int(input("Nhập số nguyên n: "))

# Kiểm tra điều kiện n < 20
if n < 20:
    # Tạo danh sách số từ 1 đến n
    so_thuan = [i for i in range(1, n+1) if i % 5 == 0 or i % 7 == 0]
    
    # In ra các số thoản mãn điều kiện
    print("Các số thoản mãn điều kiện:", so_thuan)
else:
    print("Số nhập vào phải nhỏ hơn 20")