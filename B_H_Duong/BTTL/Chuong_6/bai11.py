_list = ['abc', 'hello', 'python', 'hi', 'world']

n = int(input("Nhập n: "))

result = []

for x in _list:
    if len(x) > n:  # kiểm tra độ dài
        result.append(x)

print("Kết quả:", result)