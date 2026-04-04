_list = ['abc', 'xyz', 'aba', '1221', 'ii', 'ii2', '5yhy5']

n = int(input("Nhập n: "))

count = 0

for x in _list:
    if len(x) >= n and x[0] == x[-1]:  # điều kiện kép
        count += 1

print("Kết quả:", count)