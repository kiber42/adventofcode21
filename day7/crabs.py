def fuel_needed_simple(positions, pos):
    return sum(abs(p - pos) for p in positions)

def fuel_needed(positions, pos):
    return sum(abs(p - pos) * (abs(p - pos) + 1) // 2 for p in positions)

positions = [int(pos) for pos in open("crabs.example").read().split(",")]
print("Minimal amount of fuel needed (simple)", min(fuel_needed_simple(positions, pos) for pos in range(max(positions))))
print("Minimal amount of fuel needed (realistic)", min(fuel_needed(positions, pos) for pos in range(max(positions))))
