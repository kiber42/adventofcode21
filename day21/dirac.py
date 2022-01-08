import numpy as np

# Part 1

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

# Part 2

def turns_to_win(starting_pos):
  hist_score_pos = np.zeros((22, 10), dtype=int)
  hist_score_pos[0, starting_pos - 1] = 1
  turn = 0
  turns_to_win = np.zeros(15, dtype=int)
  while np.any(hist_score_pos):
    updated = np.zeros((22, 10))
    for pos in range(10):
      for score in range(21):
        entry = hist_score_pos[score, pos]
        if entry == 0:
          continue
        updated[min(21, score + (pos + 3) % 10 + 1), (pos + 3) % 10] += 1 * entry
        updated[min(21, score + (pos + 4) % 10 + 1), (pos + 4) % 10] += 3 * entry
        updated[min(21, score + (pos + 5) % 10 + 1), (pos + 5) % 10] += 6 * entry
        updated[min(21, score + (pos + 6) % 10 + 1), (pos + 6) % 10] += 7 * entry
        updated[min(21, score + (pos + 7) % 10 + 1), (pos + 7) % 10] += 6 * entry
        updated[min(21, score + (pos + 8) % 10 + 1), (pos + 8) % 10] += 3 * entry
        updated[min(21, score + (pos + 9) % 10 + 1), (pos + 9) % 10] += 1 * entry
    turn += 1
    turns_to_win[turn] = np.sum(updated[21, :])
    updated[21, :] = 0
    hist_score_pos = updated
  return turns_to_win


def full_game(starting_positions):
  games_won_by_A_by_duration = turns_to_win(starting_positions[0])
  games_won_by_B_by_duration = turns_to_win(starting_positions[1])
  win_count_A, win_count_B = 0, 0
  for duration in range(15):
    not_won_by_A, not_won_by_B = 1, 1
    for n in range(1, duration + 1):
      not_won_by_A = not_won_by_A * 27 - games_won_by_A_by_duration[n]
      if n == duration:
        break
      not_won_by_B = not_won_by_B * 27 - games_won_by_B_by_duration[n]
    win_count_A += games_won_by_A_by_duration[duration] * not_won_by_B
    win_count_B += games_won_by_B_by_duration[duration] * not_won_by_A
  return max(win_count_A, win_count_B)


if __name__ == "__main__":
  starting_positions = [int(line.split()[-1]) for line in open("dirac.input").readlines()]
  print("Practice game:", practice_game(starting_positions))
  print("Full game:", full_game(starting_positions))
