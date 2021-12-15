import numpy as np

class RiskMap:
  def __init__(self, filename):
    self.map = [[int(x) for x in line.strip()] for line in open(filename).readlines()]
    self.nx, self.ny = len(self.map[0]), len(self.map)
    self.nx0, self.ny0 = self.nx, self.ny

  def __getitem__(self, pos):
    x, y = pos
    excess = x // self.nx0 + y // self.ny0
    return (self.map[y % self.ny0][x % self.nx0] + excess - 1) % 9 + 1

  def grow(self):
    self.nx *= 5
    self.ny *= 5

  dirs = [(0,1), (1,0), (0,-1), (-1,0)]
  def adjacent_positions(self, pos):
    candidates = ((pos[0] + dx, pos[1] + dy) for dx, dy in RiskMap.dirs)
    return [c for c in candidates if c[0] >= 0 and c[0] < self.nx and c[1] >= 0 and c[1] < self.ny]

  def compute_distances(self):
    distances = np.zeros((self.ny, self.nx))
    updated_items = set([(0, 0)])
    while updated_items:
      start = updated_items.pop()
      for pos in self.adjacent_positions(start):
        dist_now = distances[pos]
        dist_new = distances[start] + self[pos]
        if dist_now == 0 or dist_now > dist_new:
          distances[pos] = dist_new
          updated_items.add(pos)
    return distances

if __name__ == "__main__":
  riskmap = RiskMap("chiton.example")
  print(riskmap.compute_distances())
  riskmap.grow()
  print(riskmap.compute_distances())
