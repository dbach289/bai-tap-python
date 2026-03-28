# Kiểm tra nhập đúng số nguyên dương
while True:
    try:
        n = int(input("Nhập số nguyên dương: "))
        
        if n > 0:
            break  # nhập đúng thì thoát vòng lặp
        else:
            print("Vui lòng nhập số > 0!")
    
    except:
        print("Vui lòng nhập đúng định dạng số nguyên!")

# Kiểm tra chẵn lẻ
if n % 2 == 0:
    print("Đây là một số chẵn")
else:
    print("Đây là một số lẻ")