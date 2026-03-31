# ===== Bài 1 =====
# Hàm tính tổng từ 1 đến n
def tinh_tong(n):
    # Khởi tạo biến tổng
    tong = 0
    # Dùng vòng lặp để tính tổng
    for i in range(1, n + 1):
        # Cộng i vào tổng
        tong += i
    # Trả về tổng
    return tong

# Hàm tính tổng từ 1 đến n sử dụng công thức
def tinh_tong_cong_thuc(n):
    # Công thức tính tổng: n * (n + 1) / 2
    return n * (n + 1) // 2

# Hàm main
def main():
    # Nhập số n từ người dùng
    n = int(input("Nhập số n: "))
    # Tính tổng từ 1 đến n
    tong = tinh_tong(n)
    tong_cong_thuc = tinh_tong_cong_thuc(n)
    # In kết quả
    print("Tổng từ 1 đến", n, "là:", tong)
    print("Tổng từ 1 đến", n, "sử dụng công thức là:", tong_cong_thuc)

# Chạy hàm main
if __name__ == "__main__":
    main()