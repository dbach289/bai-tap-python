# Bảng mã
code_map = {'a': '!', 'b': '@', 'c': '#', 'd': '$'}

# Tạo bảng giải mã (đảo ngược key-value)
decode_map = {v: k for k, v in code_map.items()}


def encode(text):
    result = ""
    for ch in text:
        if ch in code_map:
            result += code_map[ch]
        else:
            result += ch  # giữ nguyên nếu không có trong bảng
    return result


def decode(text):
    result = ""
    for ch in text:
        if ch in decode_map:
            result += decode_map[ch]
        else:
            result += ch
    return result


# -------- TEST --------
text = "abcd xyz"

encoded = encode(text)
decoded = decode(encoded)

print("Gốc:", text)
print("Mã hóa:", encoded)
print("Giải mã:", decoded)