def sign(n):
    return +1 if n > 0 else -1 if n < 0 else 0


class VentLine:
    def __init__(self, inputtext):
        pointA, pointB = inputtext.split(" -> ")
        self.x1, self.y1 = (int(v) for v in pointA.split(","))
        self.x2, self.y2 = (int(v) for v in pointB.split(","))
        self.dx = sign(self.x2 - self.x1)
        self.dy = sign(self.y2 - self.y1)

    def is_diagonal(self):
        return self.dx != 0 and self.dy != 0

    def __iter__(self):
        x, y = self.x1, self.y1
        yield (x, y)
        while x != self.x2 or y != self.y2:
            x += self.dx
            y += self.dy
            yield (x, y)


class VentMap:
    def __init__(self):
        # use dictionary (x,y) -> count as a sparse map
        self.counts = {}

    def load(inputtext, load_diagonals):
        vents = VentMap()
        for line in inputtext:
            ventline = VentLine(line)
            if load_diagonals or not ventline.is_diagonal():
                vents.addline(ventline)
        return vents

    def get(self, pos):
        return self.counts.get(pos, 0)

    def addpoint(self, pos):
        self.counts[pos] = self.get(pos) + 1

    def addline(self, ventline):
        for pos in ventline:
            self.addpoint(pos)

    def print(self):
        maxX = max(x for x, y in self.counts.keys())
        maxY = max(y for x, y in self.counts.keys())
        for y in range(maxY + 1):
            for x in range(maxX + 1):
                print(self.counts.get((x, y), "."), end="")
            print()


def count_dangerous(data, load_diagonals):
    vents = VentMap.load(data, load_diagonals)
    return sum(c >= 2 for c in vents.counts.values())


def main():
    data = open("vents.example").readlines()
    print("Number of dangerous positions:", count_dangerous(data, load_diagonals=False))
    print("Number of dangerous positions including diagonals:", count_dangerous(data, load_diagonals=True))


if __name__ == "__main__":
    main()
