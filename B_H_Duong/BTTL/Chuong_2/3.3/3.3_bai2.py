# Hàm nhập số nguyên dương
def nhap_so_duong(thong_bao):
    while True:
        try:
            x = int(input(thong_bao))
            if x > 0:
                return x
            else:
                print("Vui lòng nhập số > 0!")
        except:
            print("Vui lòng nhập đúng số nguyên!")

# Nhập 3 cạnh
a = nhap_so_duong("Nhập a: ")
b = nhap_so_duong("Nhập b: ")
c = nhap_so_duong("Nhập c: ")

# Kiểm tra tam giác
if a + b > c and a + c > b and b + c > a:
    print("Độ dài ba cạnh là tam giác")
else:
    print("Đây không phải độ dài ba cạnh tam giác")