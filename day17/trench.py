import math

def get_target(filename):
  line = open(filename).read().replace(",", "")
  return tuple(int(n) for token in line.split(" ")[-2:] for range in token.split("=")[-1:] for n in range.split(".."))

def generate_velocities(steps, xmin, xmax, ymin, ymax):    
  # Find allowed vx and vy ranges for each possible number of steps.
  vymin = math.ceil(ymin / steps + (steps - 1) / 2)
  vymax = math.floor(ymax / steps + (steps - 1) / 2)
  # Quadratic equation assumes that there are enough steps for x movement to come to a halt
  vxmin = math.ceil(-0.5 + (0.25 + 2 * xmin)**0.5)
  vxmax = math.floor(-0.5 + (0.25 + 2 * xmax)**0.5)
  if vxmin >= steps:
    vxmin = math.ceil(xmin / steps + (steps - 1) / 2)
  if vxmax >= steps:
    vxmax = math.floor(xmax / steps + (steps - 1) / 2)
  # Since x and y movement are independent, could just multiply possibilities values for each.
  # However, this would result in double counting in some cases, therefore explicitly generate (vx,vy) pairs.
  return ((vx, vy) for vx in range(vxmin, vxmax + 1) for vy in range(vymin, vymax + 1))


if __name__ == "__main__":
  target = get_target("trench.example")

  # Part 1 is easy to compute once you realize a few things:
  # a) movement in x is practically irrelevant
  # b) the downward velocity at y = 0 has the same magnitude as the initial velocity vy0 (at y = 0).
  # c) the (velocity for the) next step is -vy0 - 1, and it should just take you to the lower edge of the target area
  # d) the highest point is found by summing all integers from |vy0| down to 1
  ymin = target[2]
  vy0_max = -ymin - 1 # <=> -ymin = -vy0_max - 1
  print((vy0_max + 1) * vy0_max / 2)

  # Part 2
  max_steps = 2 * vy0_max + 2
  possibilities = set()
  for steps in range(1, max_steps + 1):
    possibilities.update(generate_velocities(steps, *target))
  print(len(possibilities))
