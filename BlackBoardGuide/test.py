from figureparts import Point, Box

box = Box((0, 0), (200, 190))
print(box.vertex)
print(box.width)
print(box.height)
print(box.center)
print(box.lines)
box.vertex = ((0, 10), (20, 30), (20, 40), (0, 20))
print(box)
print(box.width)
print(box.height)
print(box.center)
print(box.lines)
