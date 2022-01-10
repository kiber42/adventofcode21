class Maze:
  def __init__(self, queues, corridor, cost):
    self.queues = [list(queue) for queue in queues]
    self.corridor = list(corridor)
    self.cost = cost


  # Simplified representation, empty queues are omitted
  def __repr__(self):
    max_depth = max(len(queue) for queue in self.queues)
    lines = [
      "#" * 13,
      "#" + "".join(chr(pod + 65) if pod is not None else " " for pod in self.corridor) + "#"]
    for depth in range(max_depth):
      lines.append("  #" + "#".join(chr(queue[depth] + 65) if len(queue) > depth else " " for queue in self.queues) + "#  ")
    lines.append("  " + "#" * 9)
    return "\n".join(lines)


  # Apply move to current state
  # If move is a 3-tuple (cost, lane, corridor) => amphipod exits lane A-D to corridor tile
  # If move is an int (0-10) => amphipod from corridor tile 0-10 enters its target lane
  def apply(self, move):
    if isinstance(move, tuple):
      self.cost += move[0]
      self.corridor[move[2]] = self.queues[move[1]][0]
      del self.queues[move[1]][0]
    else:
      self.corridor[move] = None


  def load(filename, unfold):
    data = open(filename).read().strip().split("\n")
    if unfold:
      data = data[:3] + ["  #D#C#B#A#  ", "  #D#B#A#C#  "] + data[3:]
    max_depth = len(data) - 3
    # Map letters A to D to numbers, store each lane as separate list
    queues = [[ord(line[i * 2 + 3]) - ord('A') for line in data[2:-1]] for i in range(4)]
    corridor = [None] * 11
    # Pre-compute costs for leaving and entering lanes; this allows to later ignore depths altogether
    cost_to_go_up = sum(10**pod * (depth + 1) for queue in queues for depth, pod in enumerate(queue))
    cost_to_go_down = 1111 * max_depth * (max_depth + 1) // 2
    # Ignore amphipods that are already at the bottom of their target lane
    for iq, queue in enumerate(queues):
      while queue[-1] == iq:
        cost = 10**iq * len(queue)
        cost_to_go_up -= cost
        cost_to_go_down -= cost
        queue.pop()
    return Maze(queues, corridor, cost_to_go_up + cost_to_go_down)


  def is_done(self):
    return all(pos is None for pos in self.corridor) and all(len(queue) == 0 for queue in self.queues)


  def target_available(self, pod):
    return len(self.queues[pod]) == 0


  # Corridor tiles (0-10) and target lanes (A-D => 0-3) are positioned as follows:
  # 01 3 5 7 910
  #   A B C D
  def lane2pos(self, lane):
    return lane * 2 + 2


  # Test if all corridor tiles in ]start,target] are free
  def corridor_free(self, start_pos, target_pos):
    r = range(start_pos + 1, target_pos + 1) if target_pos > start_pos else range(target_pos, start_pos)
    return all(self.corridor[pos] is None for pos in r)


  def solve(self, best=1000000):
    # Moving amphipods into their final position is always correct and optimal
    move = self.find_move_into_lane()
    while move is not None:
      self.apply(move)
      move = self.find_move_into_lane()
    if self.is_done():
      if self.cost < best:
        print("Lowest energy found:", self.cost)
      return self.cost, []
    best_moves = []
    max_move_cost = best - self.cost - 1
    # Order by total cost for the horizontal movement, cheaper moves first
    for move in sorted(self.find_moves_into_corridor()):
      if move[0] > max_move_cost:
        break
      maze = Maze(self.queues, self.corridor, self.cost)
      maze.apply(move)
      result, result_moves = maze.solve(best)
      if result < best:
        best = result
        best_moves = [move] + result_moves
        max_move_cost = best - self.cost - 1
    return best, best_moves


  # Find first possible move from corridor into amphipod's target lane
  def find_move_into_lane(self):
    for start in range(11):
      pod = self.corridor[start]
      if pod is None:
        continue
      target = self.lane2pos(pod)
      if self.target_available(pod) and self.corridor_free(start, target):
        return start


  # Find all possible moves from any starting lane into intermediate position in corridor
  def find_moves_into_corridor(self):
    for lane in range(4):
      if len(self.queues[lane]) == 0:
        continue
      start = self.lane2pos(lane)
      for intermediate in range(11):
        if intermediate % 2 == 0 and intermediate % 10 != 0:
          # Not allowed to move onto 2, 4, 6, 8
          continue
        if self.corridor[intermediate] is None and self.corridor_free(start, intermediate):
          pod = self.queues[lane][0]
          target = self.lane2pos(pod)
          # Compute full cost for moving into the corridor and from there to the target lane
          yield 10**pod * (abs(intermediate - start) + abs(target - intermediate)), lane, intermediate


if __name__ == "__main__":
  for unfold in [False, True]:
    maze = Maze.load("amphipod.example", unfold)
    best, best_moves = maze.solve()
    for move in best_moves:
      maze.apply(move)
      print(maze)
    print("Solution requires", best, "energy.")
