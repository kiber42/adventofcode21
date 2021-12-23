def grow(image, blank):
  n = len(image) + 2
  return [blank * n] + [blank + row + blank for row in image] + [blank * n]

def enhance(image, enhancement, blank):
  n = len(image) + 2
  updated = [list(image[0][0] * n) for _ in range(n)]
  image = grow(image, blank)
  image = grow(image, blank)
  num_lit = 0
  for y in range(n):
    for x in range(n):
      pixel_in = int("".join(image[row][x : x + 3] for row in [y, y + 1, y + 2]), 2)
      pixel_out = enhancement[pixel_in]
      updated[y][x] = pixel_out
      if pixel_out == "1":
        num_lit += 1
  return ["".join(row) for row in updated], num_lit


def show(image):
  for row in image:
    print(row.replace("1", "#").replace("0", "."))


if __name__ == "__main__":
  enhancement, image = open("image.example").read().replace("#", "1").replace(".", "0").split("\n\n")
  image = image.split()
  image, _ = enhance(image, enhancement, "0")
  show(image)
  image, num_lit = enhance(image, enhancement, enhancement[0])
  show(image)
  print(num_lit)
  for _ in range(24):
    image, _ = enhance(image, enhancement, "0")
    image, num_lit = enhance(image, enhancement, enhancement[0])
  show(image)
  print(num_lit)
