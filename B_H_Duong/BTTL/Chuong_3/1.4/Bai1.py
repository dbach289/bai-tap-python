# ===== Bài 1 =====
# Nhập số nguyên n từ bàn phím
n = int(input("Nhập số nguyên n: "))

# In ra các giá trị của 2 nhân với các số nhỏ hơn n
print("Các giá trị của 2 nhân với các số nhỏ hơn", n, "là:")
for i in range(1, n):
    ket_qua = 2 * i
    print(f"{ket_qua} = 2*{i}")