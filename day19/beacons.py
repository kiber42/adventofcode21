from itertools import permutations
import numpy as np


def load_data(filename):
  scanner_data = open(filename).read().split("\n\n")  
  return [[np.array([int(n) for n in line.split(",")]) for line in data.split("\n")[1:] if line] for data in scanner_data]


# Produce a "90 degree" rotation matrix that aligns vec_a to vec_b
# Returns None if the resulting matrix has a negative determinant
def get_rotation(vec_a, vec_b):
  for perm in permutations(range(3)):
    vec_a_prime = np.array([vec_a[i] for i in perm])
    if np.all(abs(vec_b) == abs(vec_a_prime)):
      candidate = np.array([np.eye(3)[perm[i]] * (1 if vec_a_prime[i] == vec_b[i] else -1) for i in range(3)])
      return candidate if np.linalg.det(candidate) > 0 else None
  return None


# Find translation and rotation that maps the pair of positions in beacons_a onto those in beacons_b
def find_mapping(beacons_a, beacons_b):
    # There are two possible mappings between the two pairs; only one of them will result in a valid rotation
    rotation = get_rotation(beacons_a[1] - beacons_a[0], beacons_b[1] - beacons_b[0])
    if rotation is not None:
       offset = beacons_b[0] - np.matmul(rotation, beacons_a[0])
    else:
      rotation = get_rotation(beacons_a[0] - beacons_a[1], beacons_b[1] - beacons_b[0])
      offset = beacons_b[0] - np.matmul(rotation, beacons_a[1])
    return offset, rotation

def find_direct_mappings(scanners):
  def dist(a, b): return sum(np.square(a - b))
  distances = [[(dist(beacons[a], beacons[b]), a, b) for a in range(len(beacons)) for b in range(a)] for beacons in scanners]
  mappings = {}
  for a in range(len(scanners)):
    for b in range(a):
      overlap = set(d for d, _, _ in distances[a]).intersection(set(d for d, _, _ in distances[b]))
      # 12 common beacons -> 1+2+3+...+11 = 66 common distances; some distances might not be unique
      if len(overlap) < 50:
        continue
      # Pick random pair of matching beacons
      while True:
        selected_dist = overlap.pop()
        selected_a = [(a, b) for dist, a, b in distances[a] if dist == selected_dist]
        selected_b = [(a, b) for dist, a, b in distances[b] if dist == selected_dist]
        # Skip scenarios that are more complicated because of not unique distances (doesn't happen with my input)
        if len(selected_a) == 1 and len(selected_b) == 1:
          break
      beacons_a = [scanners[a][index] for index in selected_a[0]]
      beacons_b = [scanners[b][index] for index in selected_b[0]]
      mappings[(a, b)] = find_mapping(beacons_a, beacons_b)
      mappings[(b, a)] = find_mapping(beacons_b, beacons_a)
  return mappings


# The first scanner defines the reference coordinate system.
# Not all scanners are connected to it directly.  Combine known mappings
def find_indirect_mappings(mappings, num_scanners):
  growing = True
  while growing:
    growing = False
    for a in range(num_scanners):
      for b in range(num_scanners):
        if a == b or (a, b) in mappings:
          continue
        intermediate = next((i for i in range(0, num_scanners) if a != i and b != i and (a, i) in mappings and (i, b) in mappings), None)
        if intermediate is not None:
#          print(a, "->", intermediate, "->", b)
          offset_AI, rot_AI = mappings[(a, intermediate)]
          offset_IB, rot_IB = mappings[(intermediate, b)]
          mappings[(a, b)] = np.matmul(rot_IB, offset_AI) + offset_IB, np.matmul(rot_IB, rot_AI)
          growing = True


def combine_position_data(scanners, mappings):
  positions = list(scanners[0])
  for index, scanner in enumerate(scanners):
    if index == 0:
      continue
    offset, rot = mappings[(index, 0)]
    positions.extend(np.matmul(rot, pos) + offset for pos in scanner)
  return np.array(positions)


if __name__ == "__main__":
  scanners = load_data("beacons.example")
  mappings = find_direct_mappings(scanners)
  find_indirect_mappings(mappings, len(scanners))
  positions = combine_position_data(scanners, mappings)
  print(len(np.unique(positions, axis=0)))
  print(max(sum(abs(offset)) for offset, _ in mappings.values()))
