# ================== KHAI BÁO LỚP ==================
class BaiTap:
    def __init__(self, a, b, c):
        # Gán giá trị cho 3 biến
        self.a = a
        self.b = b
        self.c = c

    # ================== PHÉP TOÁN SỐ HỌC ==================
    def phep_toan_so_hoc(self):
        print("=== PHÉP TOÁN SỐ HỌC ===")
        print("a + b =", self.a + self.b)
        print("a - b =", self.a - self.b)
        print("a * b =", self.a * self.b)
        print("a / b =", self.a / self.b)
        print("a ** b =", self.a ** self.b)

    # ================== TOÁN TỬ QUAN HỆ ==================
    def toan_tu_quan_he(self):
        print("\n=== TOÁN TỬ SO SÁNH ===")
        print("a > b:", self.a > self.b)
        print("a < b:", self.a < self.b)
        print("a == b:", self.a == self.b)
        print("a != b:", self.a != self.b)

    # ================== TOÁN TỬ GÁN ==================
    def toan_tu_gan(self):
        print("\n=== TOÁN TỬ GÁN ===")
        x = self.a
        print("Ban đầu x =", x)

        x += self.b
        print("x += b ->", x)

        x -= self.b
        print("x -= b ->", x)

        x *= self.b
        print("x *= b ->", x)

        x /= self.b
        print("x /= b ->", x)

    # ================== TOÁN TỬ LOGIC ==================
    def toan_tu_logic(self):
        print("\n=== TOÁN TỬ LOGIC ===")
        print("(a > b) and (b > c):", (self.a > self.b) and (self.b > self.c))
        print("(a > b) or (b < c):", (self.a > self.b) or (self.b < self.c))
        print("not(a > b):", not(self.a > self.b))

    # ================== TOÁN TỬ BIT ==================
    def toan_tu_bit(self):
        print("\n=== TOÁN TỬ BIT ===")
        print("a & b =", self.a & self.b)   # AND
        print("a | b =", self.a | self.b)   # OR
        print("a ^ b =", self.a ^ self.b)   # XOR
        print("~a =", ~self.a)              # NOT
        print("a << 3 =", self.a << 3)     # Dịch trái 3 bit
        print("a >> 2 =", self.a >> 2)     # Dịch phải 2 bit

    # ================== HÀM CHẠY TẤT CẢ ==================
    def chay(self):
        self.phep_toan_so_hoc()
        self.toan_tu_quan_he()
        self.toan_tu_gan()
        self.toan_tu_logic()
        self.toan_tu_bit()


# ================== CHƯƠNG TRÌNH CHÍNH ==================
a = 16
b = 3
c = 5

bt = BaiTap(a, b, c)
bt.chay()