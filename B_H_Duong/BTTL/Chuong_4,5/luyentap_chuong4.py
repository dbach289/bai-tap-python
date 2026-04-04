def nhap_so_nguyen(thong_bao):
    while True:
        try:
            return int(input(thong_bao))
        except ValueError:
            print("Nhap sai, vui long nhap so nguyen.")


def nhap_khoang_ab():
    a = nhap_so_nguyen("Nhap a: ")
    b = nhap_so_nguyen("Nhap b: ")
    if a > b:
        a, b = b, a
    return a, b


def tong_hai_so(a, b):
    return a + b


def tong_day_so(ds):
    tong = 0
    for x in ds:
        tong += x
    return tong


def la_so_nguyen_to(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def tim_so_nguyen_to_trong_khoang(a, b):
    ket_qua = []
    i = a
    while i <= b:
        if la_so_nguyen_to(i):
            ket_qua.append(i)
        i += 1
    return ket_qua


def la_so_hoan_hao(n):
    if n <= 1:
        return False
    tong_uoc = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            tong_uoc += i
            if i != n // i:
                tong_uoc += n // i
        i += 1
    return tong_uoc == n


def tim_so_hoan_hao_trong_khoang(a, b):
    ket_qua = []
    i = a
    while i <= b:
        if la_so_hoan_hao(i):
            ket_qua.append(i)
        i += 1
    return ket_qua


def bai_1():
    print("\n=== Bai 1: Tinh tong 2 so ===")
    x = nhap_so_nguyen("Nhap so thu nhat: ")
    y = nhap_so_nguyen("Nhap so thu hai: ")
    print(f"Tong = {tong_hai_so(x, y)}")


def bai_2():
    print("\n=== Bai 2: Tinh tong cac so truyen vao ===")
    n = nhap_so_nguyen("Nhap so luong phan tu n: ")
    while n <= 0:
        print("n phai > 0")
        n = nhap_so_nguyen("Nhap lai n: ")

    ds = []
    i = 1
    while i <= n:
        ds.append(nhap_so_nguyen(f"Nhap phan tu thu {i}: "))
        i += 1
    print(f"Tong day so = {tong_day_so(ds)}")


def bai_3():
    print("\n=== Bai 3: Kiem tra so nguyen to ===")
    n = nhap_so_nguyen("Nhap n: ")
    if la_so_nguyen_to(n):
        print(f"{n} la so nguyen to.")
    else:
        print(f"{n} khong phai la so nguyen to.")


def bai_4():
    print("\n=== Bai 4: Tim so nguyen to trong [a, b] ===")
    a, b = nhap_khoang_ab()
    ds_snt = tim_so_nguyen_to_trong_khoang(a, b)
    if ds_snt:
        print("Cac so nguyen to:", ds_snt)
    else:
        print("Khong co so nguyen to nao trong khoang.")


def bai_5():
    print("\n=== Bai 5: Kiem tra so hoan hao ===")
    n = nhap_so_nguyen("Nhap n: ")
    if la_so_hoan_hao(n):
        print(f"{n} la so hoan hao.")
    else:
        print(f"{n} khong phai la so hoan hao.")


def bai_6():
    print("\n=== Bai 6: Tim so hoan hao trong [a, b] ===")
    a, b = nhap_khoang_ab()
    ds_shh = tim_so_hoan_hao_trong_khoang(a, b)
    if ds_shh:
        print("Cac so hoan hao:", ds_shh)
    else:
        print("Khong co so hoan hao nao trong khoang.")


def in_menu():
    print("\n========== MENU LUYEN TAP CHUONG 4 ==========")
    print("1. Viet ham tinh tong 2 so truyen vao")
    print("2. Viet ham tinh tong cac so truyen vao")
    print("3. Viet ham kiem tra mot so nguyen to")
    print("4. Viet chuong trinh tim cac so nguyen to trong [a, b]")
    print("5. Viet ham kiem tra so hoan hao")
    print("6. Viet chuong trinh tim cac so hoan hao trong [a, b]")
    print("0. Thoat")


def chuong_trinh_chinh():
    while True:
        in_menu()
        lua_chon = nhap_so_nguyen("Nhap lua chon cua ban: ")

        if lua_chon == 1:
            bai_1()
        elif lua_chon == 2:
            bai_2()
        elif lua_chon == 3:
            bai_3()
        elif lua_chon == 4:
            bai_4()
        elif lua_chon == 5:
            bai_5()
        elif lua_chon == 6:
            bai_6()
        elif lua_chon == 0:
            print("Tam biet!")
            break
        else:
            print("Lua chon khong hop le, vui long nhap lai.")


if __name__ == "__main__":
    chuong_trinh_chinh()
