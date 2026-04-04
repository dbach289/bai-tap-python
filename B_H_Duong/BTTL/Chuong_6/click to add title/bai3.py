_tuple = ('ab', 'b', 'e', 'c', 'd', 'e', 'ab')

_new_tuple = ()

for x in _tuple:
    if x not in _new_tuple:  # chưa có thì thêm
        _new_tuple += (x,)

print(_new_tuple)