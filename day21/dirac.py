class DeterministicDie:
  def __init__(self):
    self.val = 0
    self.num_rolls = 0

  def __call__(self):
    result = 3 * self.val + 6
    if result > 297:
      result -= 100      
    self.val = (self.val + 2) % 100 + 1
    self.num_rolls += 3
    return result


class DiracDie:
  def __init__(self):
    self.current = None
    self.index = 0
    self.queue = [()]

  def done(self):
    return len(self.queue) == 0
  
  def deterministic(self):
    return len(self.current) > self.index

  def next_universe(self):
    self.current = self.queue.pop()
    self.index = 0

  # returns either a deterministic sequence of a previously create universe
  # or creates new universes and steps into first one
  def __call__(self):
    if self.index < len(self.current):
      index = self.index
      self.index = len(self.current)
      return self.current[index:]
    self.queue.append(self.current + (9,)) # 3,3,3
    self.queue.extend([self.current + (8,)] * 3) # 2,3,3 (x3)
    self.queue.extend([self.current + (7,)] * 6) # 1,3,3 (x3), 2,2,3 (x3)
    self.queue.extend([self.current + (6,)] * 7) # 1,2,3 (x6), 2,2,2
    self.queue.extend([self.current + (5,)] * 6) # 1,2,2 (x3), 1,1,3 (x3)
    self.queue.extend([self.current + (4,)] * 3) # 1,1,2 (x3)
    self.current += (3,)
    self.index += 1
    return (3,)
    

class CachedComputation:
  def __init__(self, compute_fn, **kwargs):
    self.cache = {}
    self.compute = compute_fn
    self.kwargs = kwargs

  def __call__(self, *args):
    try:
      return self.cache[args]
    except KeyError:
      self.cache[args] = result = self.compute(*args, **self.kwargs)
      return result


def practice_game(starting_positions):
  posA, posB = starting_positions
  scoreA, scoreB = 0, 0
  dd = DeterministicDie()
  while True:
    posA += dd()
    posA = (posA - 1) % 10 + 1
    scoreA += posA
    if scoreA >= 1000:
      return scoreB * dd.num_rolls
    posB += dd()
    posB = (posB - 1) % 10 + 1
    scoreB += posB
    if scoreB >= 1000:
      return scoreA * dd.num_rolls
  

def do_apply_rolls(pos, score, *rolls):
  turns = 0
  n = len(rolls)
  while score < 21 and turns < n:
    pos += rolls[turns]
    pos = (pos - 1) % 10 + 1
    score += pos
    turns += 1
  return pos, score, turns


def turns_to_win(starting_position, apply_rolls):
  dd = DiracDie()
  num_turns = [0] * 22
  count = 0
  while not dd.done():
    pos, score, turns = starting_position, 0, 0
    dd.next_universe()
    count += 1
    if count % 500000 == 0:
      print(count, len(dd.queue))
    while score < 21:
      rolls = dd()
      pos, score, turns_used = apply_rolls(pos, score, *rolls)
      turns += turns_used
    num_turns[turns] += 1
  return num_turns

def count_wins(games_won_by_A_by_duration, games_won_by_B_by_duration):
  win_count_A, win_count_B = 0, 0
  for duration in range(2, 22):
    not_won_by_A, not_won_by_B = 1, 1
    for n in range(1, duration + 1):
      not_won_by_A = not_won_by_A * 27 - games_won_by_A_by_duration[n]
      if n == duration:
        break
      not_won_by_B = not_won_by_B * 27 - games_won_by_B_by_duration[n]
    win_count_A += games_won_by_A_by_duration[duration] * not_won_by_B
    win_count_B += games_won_by_B_by_duration[duration] * not_won_by_A
  return win_count_A, win_count_B


def full_game(starting_positions):
  apply_rolls = CachedComputation(do_apply_rolls)
  games_won_by_A_by_duration = turns_to_win(starting_positions[0], apply_rolls)
  games_won_by_B_by_duration = turns_to_win(starting_positions[1], apply_rolls)  
  win_count_A, win_count_B = count_wins(games_won_by_A_by_duration, games_won_by_B_by_duration)
  print(games_won_by_A_by_duration)
  print(games_won_by_B_by_duration)
  print("A wins", win_count_A, "times")
  print("B wins", win_count_B, "times")
  return max(win_count_A, win_count_B)


if __name__ == "__main__":
  starting_positions = [int(line.split()[-1]) for line in open("dirac.example").readlines()]
  print(practice_game(starting_positions))
  print(full_game(starting_positions))
