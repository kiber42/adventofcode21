def most_common(values, pos):
    return sum(value[pos] for value in values) >= len(values) / 2

def least_common(values, pos):
    return 1 - most_common(values, pos)

def from_binary(bits):
    return sum(b << i for i, b in enumerate(reversed(bits)))


data = open("rating.example").read().strip().split("\n")
values = [[int(b) for b in line] for line in data]

# Part 1
n = len(values[0])
gamma = from_binary([most_common(values, b) for b in range(n)])
epsilon = from_binary([least_common(values, b) for b in range(n)])
print("Power consumption:", gamma * epsilon)

# Part 2
oxygen = values
for b in range(n):
    selected = most_common(oxygen, b)
    oxygen = [value for value in oxygen if value[b] == selected]
    if len(oxygen) == 1:
        break

scrubber = values
for b in range(n):
    selected = least_common(scrubber, b)
    scrubber = [value for value in scrubber if value[b] == selected]
    if len(scrubber) == 1:
        break

oxygen = from_binary(oxygen[0])
scrubber = from_binary(scrubber[0])
print("Oxygen rating:", oxygen)
print("CO2 scrubber rating:", scrubber)
print("Life support rating:", oxygen * scrubber)
