# ===== Bài 2 =====
# Ghi đoạn văn bản vào tập tin rồi hiển thị lại nội dung đó.

import os

_THU_MUC = os.path.dirname(os.path.abspath(__file__))
_FILE_OUT = os.path.join(_THU_MUC, "bai2_output.txt")


def main() -> None:
    van_ban = input("Nhap doan van ban: ")
    with open(_FILE_OUT, "w", encoding="utf-8") as f:
        f.write(van_ban)
    with open(_FILE_OUT, "r", encoding="utf-8") as f:
        doc = f.read()
    print("Noi dung da ghi va doc lai tu file:")
    print(doc)


if __name__ == "__main__":
    main()
