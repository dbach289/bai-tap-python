# ===== Bài 3 =====
# Hàm kiểm tra số nguyên tố 

def kiem_tra_nguyen_to(n):
    # Số nhỏ hơn 2 không phải là số nguyên tố
    if n < 2:
        return False
    
    i = 2
    while i <= int(n**0.5):
        if n % i == 0:
            return False
        i += 1
    
    return True


# Nhập số nguyên dương từ bàn phím (có kiểm tra lỗi)
while True:
    try:
        n = int(input("Nhập số nguyên dương: "))
        if n < 0:
            print("Phải nhập số >= 0!")
        else:
            break
    except:
        print("Nhập sai, nhập lại!")


# Kiểm tra và in kết quả
if kiem_tra_nguyen_to(n):
    print("Đây là số nguyên tố")
else:
    print("Không phải số nguyên tố")