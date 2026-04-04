# ===== Bài 1 =====
# Đọc n dòng đầu tiên của một tập tin cho trước (n nhập từ bàn phím).

def main() -> None:
    n = int(input("Nhap n (so dong can doc): "))
    duong_dan = input("Nhap duong dan file: ").strip().strip('"')
    with open(duong_dan, "r", encoding="utf-8") as f:
        for i, dong in enumerate(f):
            if i >= n:
                break
            print(dong, end="")


if __name__ == "__main__":
    main()
