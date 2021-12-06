data = open("lanternfish.example").read()
fishes=[0] * 9
for f in data.split(","):
    fishes[int(f)] += 1
for day in range(257):
    print("Number of fish after {} days: {}".format(day, sum(fishes)))
    fishes = fishes[1:] + [fishes[0]]
    fishes[6] += fishes[-1]
