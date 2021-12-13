class Octopuses:
  def __init__(self, filename):
    self.energies = [[int(x) for x in line.strip()] for line in open(filename).readlines()]
    self.nx, self.ny = len(self.energies[0]), len(self.energies)
    self.step_count = 0

  def energy(self, pos):
    return self.energies[pos[1]][pos[0]]

  def increase(self, pos):
    x, y = pos
    self.energies[y][x] += 1
    return self.energies[y][x]

  def clear_flashed(self, pos):
    x, y = pos
    if self.energies[y][x] >= 10:
      self.energies[y][x] = 0

  def print(self):
    for y in range(self.ny):
      for x in range(self.nx):
        print(self.energy((x, y)), end="")
      print()
    print("-" * self.nx)

  def adjacent_positions(self, pos):
    dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    candidates = ((pos[0] + dx, pos[1] + dy) for dx, dy in dirs)
    return [c for c in candidates if c[0] >= 0 and c[0] < self.nx and c[1] >= 0 and c[1] < self.ny]

  def one_step(self):
    will_flash = []
    num_flashes = 0
    for y in range(self.ny):
      for x in range(self.nx):
        pos = x,y
        self.increase(pos)
        if self.energy(pos) == 10:
          will_flash.append(pos)
    while will_flash:
      num_flashes += 1
      flashing = will_flash.pop()
      for pos in self.adjacent_positions(flashing):
        if self.increase(pos) == 10:
          will_flash.append(pos)
    for y in range(self.ny):
      for x in range(self.nx):
        self.clear_flashed((x, y))
    self.step_count += 1
    return num_flashes

  def process(self, num_steps = 100):
    flashes_total = 0
    for _ in range(num_steps):
      num_flashes = self.one_step()
      flashes_total += num_flashes
      if num_flashes == self.nx * self.ny:
        return self.step_count
      if self.step_count < 10 or self.step_count % 10 == 0:
        print("After {} step(s)".format(self.step_count))
        self.print()
    return flashes_total


if __name__ == "__main__":
  octopuses = Octopuses("octopus.input")
  print("Number of flashes in 100 steps:", octopuses.process(100))
  print("Number of steps until first full flash:", octopuses.process(1000))
