class Bai2:
    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    # Hàm thực hiện toán tử so sánh
    def toan_tu_so_sanh(self):
        print("=== TOÁN TỬ SO SÁNH ===")
        print("s1 > s2:", self.s1 > self.s2)
        print("s1 < s2:", self.s1 < self.s2)
        print("s1 == s2:", self.s1 == self.s2)
        print("s1 != s2:", self.s1 != self.s2)

        print("s2 > s3:", self.s2 > self.s3)
        print("s2 < s3:", self.s2 < self.s3)
        print("s2 == s3:", self.s2 == self.s3)
        print("s2 != s3:", self.s2 != self.s3)

    # Hàm thực hiện toán tử logic
    def toan_tu_logic(self):
        print("\n=== TOÁN TỬ LOGIC ===")
        print("(s1 < s2) and (s2 < s3):", (self.s1 < self.s2) and (self.s2 < self.s3))
        print("(s1 > s2) or (s2 < s3):", (self.s1 > self.s2) or (self.s2 < self.s3))
        print("not(s1 < s2):", not (self.s1 < self.s2))


# Chạy chương trình
obj = Bai2('a', 'b', 'c')

obj.toan_tu_so_sanh()
obj.toan_tu_logic()