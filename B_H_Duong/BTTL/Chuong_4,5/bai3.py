# ===== Bài 3 =====
# Tao demo_file1.txt trong thu muc source; noi dung theo de bai.
# a) In noi dung tren mot dong.
# b) In noi dung tung dong.

import os

_THU_MUC = os.path.dirname(os.path.abspath(__file__))
_DEMO = os.path.join(_THU_MUC, "demo_file1.txt")
# Noi dung: Thuc \n hanh \n voi \n file\n IO\n
_NOI_DUNG = "Thuc \nhanh \nvoi \nfile\n IO\n"


def main() -> None:
    with open(_DEMO, "w", encoding="utf-8") as f:
        f.write(_NOI_DUNG)

    with open(_DEMO, "r", encoding="utf-8") as f:
        toan_bo = f.read()

    print("a) Tren mot dong:")
    # Gop cac dong thanh mot dong (thay xuong dong bang khoang trang)
    mot_dong = " ".join(line.rstrip("\n\r") for line in toan_bo.splitlines())
    print(mot_dong)

    print("\nb) Tung dong:")
    with open(_DEMO, "r", encoding="utf-8") as f:
        for dong in f:
            print(dong, end="")


if __name__ == "__main__":
    main()
