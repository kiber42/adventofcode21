class Landscape:
  def __init__(self, filename):
    self.heights = [[int(x) for x in line.strip()] for line in open(filename).readlines()]
    self.nx, self.ny = len(self.heights[0]), len(self.heights)

  def height(self, pos):
    return self.heights[pos[1]][pos[0]]

  def print(self):
    for y in range(self.ny):
      for x in range(self.nx):
        pos = x, y
        print(self.height(pos) if not self.is_marked(pos) else "x", end="")
      print()
    print("-" * self.nx)

  def adjacent_positions(self, pos):
    x, y = pos
    candidates = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
    return [c for c in candidates if c[0] >= 0 and c[0] < self.nx and c[1] >= 0 and c[1] < self.ny]

  def is_local_min(self, pos):
    local = self.height(pos)
    return min(self.height(p) for p in self.adjacent_positions(pos)) > local

  def find_minima(self):
    return [(x, y) for x in range(self.nx) for y in range(self.ny) if self.is_local_min((x, y))]

  def mark_position(self, pos):    
    self.heights[pos[1]][pos[0]] += 10

  def is_marked(self, pos):    
    return self.height(pos) >= 9

  def find_starting_position(self):
    return next(((x, y) for x in range(self.nx) for y in range(self.ny) if not self.is_marked((x, y))), None)

  def find_basin(self, start):
    size = 0
    queue = [start]
    while queue:
      pos = queue.pop()
      if self.is_marked(pos):
        continue
      size += 1
      self.mark_position(pos)
      queue.extend(self.adjacent_positions(pos))
#      self.print()
    return size

  def find_all_basins(self):
    basins = []
    while True:
      start = self.find_starting_position()
      if not start:
        break
      basin_size = self.find_basin(start)
      basins.append(basin_size)
    return basins


def main():
  landscape = Landscape("basin.input")
  risk = sum(landscape.height(pos) + 1 for pos in landscape.find_minima())
  print("Risk level:", risk)
  basins = landscape.find_all_basins()
  largest = sorted(basins)[-3:]
  print(largest, "=>", largest[0] * largest[1] * largest[2])


if __name__ == "__main__":
  main()
