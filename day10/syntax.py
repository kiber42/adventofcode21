matching = {")": "(", "]": "[", "}": "{", ">": "<"}

def corruption_score(line):
  scores = {")": 3, "]": 57, "}": 1197, ">" : 25137}
  openings = []
  for char in line:
    if char in "([{<":
      openings.append(char)
    elif openings[-1] != matching[char]:
      return scores[char]
    else:
      openings.pop()
  return 0


def completion_score(line):
  openings = []
  for char in line:
    if char in "([{<":
      openings.append(char)
    elif openings[-1] != matching[char]:
      return None
    else:
      openings.pop()
  return compute_completion_score(openings)


def compute_completion_score(openings):
  scores = {"(": 1, "[": 2, "{": 3, "<" : 4}
  score = 0
  for token in reversed(openings):
    score *= 5
    score += scores[token]
  return score


def middle(items):
  items = sorted(item for item in items if item is not None)
  return items[len(items) // 2]


lines = [line.strip() for line in open("syntax.example").readlines()]
print(sum(corruption_score(line) for line in lines))
print(middle(completion_score(line) for line in lines))
