# ===== Bài 4 =====
# Nhap thong tin ca nhan, luu setInfo.txt, doc lai va hien thi.

import os

_THU_MUC = os.path.dirname(os.path.abspath(__file__))
_SET_INFO = os.path.join(_THU_MUC, "setInfo.txt")


def main() -> None:
    ten = input("Ten: ")
    tuoi = input("Tuoi: ")
    email = input("Email: ")
    skype = input("Skype: ")
    dia_chi = input("Dia chi: ")
    noi_lam_viec = input("Noi lam viec: ")

    noi_dung = (
        f"Ten: {ten}\n"
        f"Tuoi: {tuoi}\n"
        f"Email: {email}\n"
        f"Skype: {skype}\n"
        f"Dia chi: {dia_chi}\n"
        f"Noi lam viec: {noi_lam_viec}\n"
    )

    with open(_SET_INFO, "w", encoding="utf-8") as f:
        f.write(noi_dung)

    print("\n(b) Doc lai tu setInfo.txt:\n")
    with open(_SET_INFO, "r", encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()
