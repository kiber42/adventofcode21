import numpy as np

data = open("seacucumbers.example").readlines()
field = np.array([[0 if char == "." else (1 if char == ">" else 2)
                   for char in row.strip()] for row in data])

ny, nx = field.shape
turns = 0
while True:
    moved = False
    previous = field
    field = np.zeros(field.shape)
    for y in range(ny):
        for x in range(nx):
            prev = previous[y][x]
            if prev == 0:
                continue
            if prev == 1 and previous[y][(x + 1) % nx] == 0:                
                field[y][(x + 1) % nx] = 1
                moved = True
            else:
                field[y][x] = prev
    previous = field
    field = np.zeros(field.shape)
    for y in range(ny):
        for x in range(nx):
            prev = previous[y][x]
            if prev == 0:
                continue
            if previous[y][x] == 2 and previous[(y + 1) % ny][x] == 0:
                field[(y + 1) % ny][x] = 2
                moved = True
            else:
                field[y][x] = prev
    turns += 1
    if not moved:
        break

print("No more movement after", turns, "turns.")
