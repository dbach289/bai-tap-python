class hocvien:
    def __init__(self, hoten, ngaysinh, email, dienthoai, diachi, lop):
        self.hoten = hoten
        self.ngaysinh = ngaysinh
        self.email = email
        self.dienthoai = dienthoai
        self.diachi = diachi
        self.lop = lop

    def show_info(self):
        print("Họ tên:", self.hoten)
        print("Ngày sinh:", self.ngaysinh)
        print("Email:", self.email)
        print("Điện thoại:", self.dienthoai)
        print("Địa chỉ:", self.diachi)
        print("Lớp:", self.lop)

    def change_info(self, diachi="Hà Nội", lop="IT12.x"):
        self.diachi = diachi
        self.lop = lop


class Main:
    def run():
        hv = hocvien("Nguyễn Văn A", "01/01/2000", "a@gmail.com", "090000", "Hà Nam", "CNTT1")

        hv.show_info()
        print("------")

        hv.change_info()
        hv.show_info()
        print("------")

        hv.change_info("Bắc Ninh", "CNTT2")
        hv.show_info()


Main.run()