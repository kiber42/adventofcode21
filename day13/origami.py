def load_dots_and_instructions(data):
  dots = set()
  processed = 0
  for line in data:
    line = line.strip()
    processed += 1
    if not line:
      break
    dots.add(tuple(int(v) for v in line.split(",")))
  folds = []
  for line in data[processed:]:
    instruction = line.split(" ")[-1]
    axis, pos = instruction.split("=")
    folds.append((axis, int(pos)))
  return dots, folds


def fold_x(dots, fold):
  return set(((fold_if(dot[0], fold), dot[1]) for dot in dots))

def fold_y(dots, fold):
  return set(((dot[0], fold_if(dot[1], fold)) for dot in dots))

def fold_if(value, fold):
  return 2 * fold - value if value > fold else value


def apply(dots, instruction):
  axis, fold = instruction
  if axis == "x":
    return fold_x(dots, fold)
  else:
    return fold_y(dots, fold)


def show(dots):
  nx = max(dot[0] for dot in dots) + 1
  ny = max(dot[1] for dot in dots) + 1
  for y in range(ny):
    for x in range(nx):
      print("*" if (x, y) in dots else " ", end="")
    print()


if __name__ == "__main__":
  data = open("origami.input").readlines()
  dots, instructions = load_dots_and_instructions(data)
  dots = apply(dots, instructions[0])
  print(len(dots))
  for instruction in instructions[1:]:
    dots = apply(dots, instruction)
  show(dots)
