# ===== Bài 4 =====
# Hàm kiểm tra số chia hết cho 2 hoặc 3
def kiem_tra_so(n):
    # Kiểm tra số chia hết cho 2
    if n % 2 == 0:
        # Kiểm tra số chia hết cho 3
        if n % 3 == 0:
            return f"Số {n} chia hết cho cả 2 và 3"
        else:
            return f"Số {n} chia hết cho 2 nhưng không chia hết cho 3"
    # Kiểm tra số chia hết cho 3
    elif n % 3 == 0:
        return f"Số {n} chia hết cho 3 nhưng không chia hết cho 2"
    else:
        return f"Số {n} không chia hết cho cả 2 và 3"

# Nhập số nguyên dương
so_nguyen = int(input("Nhập số nguyên dương: "))

# Kiểm tra số nguyên dương
if so_nguyen > 0:
    print(kiem_tra_so(so_nguyen))
else:
    print("Số nhập vào không phải là số nguyên dương")