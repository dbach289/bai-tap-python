# ===== Bài 2 =====
# Nhập số nguyên từ bàn phím
n = int(input("Nhập số nguyên: "))

# Kiểm tra số nhập vào
if n > 10:
    # In thông báo nếu số nhập vào lớn hơn 10
    print("Số nhập vào phải bé hơn 10")
else:
    # In ra những số chẵn trong khoảng từ 1 đến n
    print("Những số chẵn trong khoảng từ 1 đến", n, "là:")
    for i in range(1, n + 1):
        # Kiểm tra số chẵn
        if i % 2 == 0:
            print(i)