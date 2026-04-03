# ===== Bài 2 =====
# Hàm tính giai thừa

def tinh_giai_thua(n):
    # Kiểm tra đầu vào
    if not isinstance(n, int) or n < 0:
        return "Vui lòng nhập số nguyên dương"
    
    # Trường hợp đặc biệt
    if n == 0 or n == 1:
        return 1
    
    # Tính giai thừa bằng while
    giai_thua = 1
    i = 2
    while i <= n:
        giai_thua *= i
        i += 1
    
    return giai_thua


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


# In kết quả
print(f"{n}! = {tinh_giai_thua(n)}")