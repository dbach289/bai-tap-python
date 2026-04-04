_tuple = ('a', 'b', 'd', 'e')

# chèn 'c' vào vị trí index 2
_new_tuple = _tuple[:2] + ('c',) + _tuple[2:]

print(_new_tuple)