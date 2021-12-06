commands = open("pilot.example").readlines()
x, depth, aim = 0, 0, 0
for line in commands:
    command, n = line.split(" ")
    n = int(n)
    if command == "forward":
        x += n
        depth += aim * n
    elif command == "down":
        aim += n
    else:
        aim -= n
print("X = {}, Aim = {}, Depth = {}".format(x, aim, depth))
print("X * Aim = {}, X * Depth = {}".format(x*aim, x*depth))
