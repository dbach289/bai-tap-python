# ===== Bài 5 =====
# File demo_file2.txt; dem so lan xuat hien moi tu (dictionary).

import os
from collections import Counter

_THU_MUC = os.path.dirname(os.path.abspath(__file__))
_DEMO2 = os.path.join(_THU_MUC, "demo_file2.txt")
# Noi dung theo de: "Dem so luong tu xuat hien abc abc abc 12 12 it it eaut"
_VAN_BAN_MAU = "Dem so luong tu xuat hien abc abc abc 12 12 it it eaut"


def main() -> None:
    with open(_DEMO2, "w", encoding="utf-8") as f:
        f.write(_VAN_BAN_MAU)

    with open(_DEMO2, "r", encoding="utf-8") as f:
        text = f.read()

    tu = text.split()
    ket_qua = dict(Counter(tu))
    print(ket_qua)


if __name__ == "__main__":
    main()
