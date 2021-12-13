def find_connections(filename):
  connections = {}
  for connection in open(filename).readlines():
    source, dest = connection.strip().split("-")
    if not source in connections:
      connections[source] = set()
    if not dest in connections:
      connections[dest] = set()
    connections[source].add(dest)
    connections[dest].add(source)
  return connections


def find_paths_from(pos, connections, may_visit_twice = 0, visited_small = set()):
  visited_small = set(visited_small)
  if pos.lower() == pos:
    visited_small.add(pos)
  segments = []
  for dest in connections[pos]:
    if dest == "start":
      continue
    if dest == "end":
      segments.append(dest)
      continue
    if dest in visited_small:
      if may_visit_twice > 0:
        segments.extend(dest + "," + seg for seg in find_paths_from(dest, connections, may_visit_twice - 1, visited_small))
      continue
    segments.extend(dest + "," + seg for seg in find_paths_from(dest, connections, may_visit_twice, visited_small))
  return segments


if __name__ == "__main__":
  connections = find_connections("path.example")
  paths_a = find_paths_from("start", connections)
  print(len(paths_a))
  paths_b = find_paths_from("start", connections, 1)
  print(len(paths_b))
