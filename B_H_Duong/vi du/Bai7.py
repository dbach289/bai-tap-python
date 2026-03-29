# ===== Bài 7 =====
# Hàm kiểm tra số nguyên tố
def is_prime(n):
    # Số nguyên tố phải lớn hơn 1
    if n <= 1:
        return False
    # Kiểm tra từ 2 đến căn bậc 2 của n
    for i in range(2, int(n**0.5) + 1):
        # Nếu n chia hết cho bất kỳ số nào trong khoảng này, thì không phải số nguyên tố
        if n % i == 0:
            return False
    # Nếu không chia hết cho bất kỳ số nào, thì là số nguyên tố
    return True

# Nhập số nguyên dương
n = int(input("Nhập một số nguyên dương: "))

# Kiểm tra và in kết quả
if is_prime(n):
    print(f"{n} là số nguyên tố")
else:
    print(f"{n} không phải là số nguyên tố")