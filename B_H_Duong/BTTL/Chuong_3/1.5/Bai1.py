# ===== Bài 1 =====
# Tính và in ra Ước của 10 số tự nhiên đầu tiên

def uoc_so(n):
    uoc = []
    i = 1
    while i <= n:
        if n % i == 0:
            uoc.append(i)
        i += 1
    return uoc

# In ra ước số của 10 số tự nhiên đầu tiên
i = 1
while i <= 10:
    print(f"Ước số của {i}: {uoc_so(i)}")
    i += 1