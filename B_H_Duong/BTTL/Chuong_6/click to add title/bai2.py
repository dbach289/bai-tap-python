_tuple = ('ab', 'b', 'e', 'c', 'd', 'e', 'ab')

_new_tuple = ()

for x in _tuple:
    if _tuple.count(x) == 1:  # chỉ lấy phần tử xuất hiện 1 lần
        _new_tuple += (x,)

print(_new_tuple)