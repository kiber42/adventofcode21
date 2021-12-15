import numpy as np

class CachedComputation:
  def __init__(self, compute_fn, **kwargs):
    self.cache = {}
    self.compute = compute_fn
    self.kwargs = kwargs

  def __call__(self, *args):
    try:
      return self.cache[args]
    except KeyError:
      self.cache[args] = result = self.compute(self, *args, **self.kwargs)
      return result


def get_insertion_counts(compute, fragment, num_rounds, rules):
  replacement = rules.get(fragment, "") if num_rounds > 0 else ""
  if not replacement:
    counts = np.zeros(26)
    counts[ord(fragment[0]) - 65] = 1
    return counts
  return compute(fragment[0] + replacement, num_rounds - 1) + compute(replacement + fragment[1], num_rounds - 1)


if __name__ == "__main__":
  data = open("polymer.example").readlines()
  rules = dict(line.strip().split(" -> ") for line in data[2:])
  template = data[0].strip()
  insertion_counts = CachedComputation(get_insertion_counts, rules=rules)
  for rounds in [10, 40]:
    counts = sum(insertion_counts(template[index:index+2], rounds) for index in range(len(template)))
    nonzero = sorted(counts[counts>0])
    print(int(nonzero[-1] - nonzero[0]))
 