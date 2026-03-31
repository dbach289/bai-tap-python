# ===== Bài 3 =====
# Tạo danh sách các số từ 80 đến 100
ds_so = list(range(80, 101))

# Lọc các số vừa chia hết cho 2, vừa chia hết cho 3
ds_so_thoa_man = [so for so in ds_so if so % 2 == 0 and so % 3 == 0]

# In ra các số thỏa mãn điều kiện
print("Các số từ 80 đến 100 vừa chia hết cho 2, vừa chia hết cho 3 là:")
for so in ds_so_thoa_man:
    print(so)