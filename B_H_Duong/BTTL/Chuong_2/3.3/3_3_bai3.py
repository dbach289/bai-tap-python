import time

# Hàm nhập năm sinh hợp lệ
def nhap_nam_sinh():
    while True:
        try:
            ns = int(input("Nhập năm sinh: "))
            
            # Lấy năm hiện tại
            nam_hien_tai = time.localtime()[0]
            
            if 1900 <= ns <= nam_hien_tai:
                return ns
            else:
                print("Năm sinh không hợp lệ!")
        except:
            print("Vui lòng nhập đúng số!")

# Nhập năm sinh
nam_sinh = nhap_nam_sinh()

# Lấy năm hiện tại
nam_hien_tai = time.localtime()[0]

# Tính tuổi
tuoi = nam_hien_tai - nam_sinh

# In kết quả
print(f"Năm sinh {nam_sinh}, vậy bạn {tuoi} tuổi")