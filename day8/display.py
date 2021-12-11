# Part 1
def process_line_basic(line):
    _, code = line.strip().split(" | ")
    num_unique_digits = sum(1 for token in code.split()
                            if len(token) in [2, 3, 4, 7])
    print(num_unique_digits, end=" ")
    return num_unique_digits

# Part 2
# 0 => 6 a b c   e f g
# 1 => 2     c     f
# 2 => 5 a   c d e   g
# 3 => 5 a   c d   f g
# 4 => 4   b c d   f
# 5 => 5 a b   d   f g
# 6 => 6 a b   d e f g
# 7 => 3 a   c     f
# 8 => 7 a b c d e f g
# 9 => 6 a b c d   f g
# SUM    8 6 8 7 4 9 7
# COUNT is unique for 1, 4, 7, 8
# SUM is unique for b, e, f
#
# 1.) Identify unique numbers 1, 4, 7, 8
# 2.) Split into groups that do/don't contain "1" (0,3,9 / 2,5,6)
# 3.) Identify 3 (contains "1", 5 segments) and 6 (doesn't contain "1", 6 segments)
# 4.) Identify "e" (appears 4 times only)
# 5.) Identify 0 vs. 9 (contains "1", "e" vs not "e") and 2 vs 5 (don't contain "1", "e" vs not "e")


def process_line_full(line):
    all_patterns, code = line.strip().split(" | ")
    mapping = decode(all_patterns)
    digits = [mapping["".join(sorted(x))] for x in code.split()]
    value = sum(d * 10**i for i, d in enumerate(reversed(digits)))
    print(value, end=" ")
    return value


def contains(pattern, subpattern):
    return all(segment in pattern for segment in subpattern)


def decode(all_patterns):
    patterns = ["".join(sorted(pattern)) for pattern in all_patterns.split()]
    def find(length): return next(p for p in patterns if len(p) == length)
    unique = {1: find(2), 4: find(4), 7: find(3), 8: find(7)}
    not_unique = [p for p in patterns if not p in unique.values()]
    group_039 = [p for p in not_unique if contains(p, unique[1])]
    group_256 = [p for p in not_unique if not contains(p, unique[1])]
    letters = [chr(ord("a") + n) for n in range(7)]
    segment_counts = [all_patterns.count(l) for l in letters]
    e = next(letters[i] for i in range(7) if segment_counts[i] == 4)
    return {
        next(p for p in group_039 if e in p): 0,
        unique[1]: 1,
        next(p for p in group_256 if len(p) == 5 and e in p): 2,
        next(p for p in group_039 if len(p) == 5): 3,
        unique[4]: 4,
        next(p for p in group_256 if not e in p): 5,
        next(p for p in group_256 if len(p) == 6): 6,
        unique[7]: 7,
        unique[8]: 8,
        next(p for p in group_039 if len(p) == 6 and not e in p): 9
    }


def main():
    data = open("display.example").readlines()
    print("=>", sum(process_line_basic(line) for line in data))
    print("=>", sum(process_line_full(line) for line in data))


if __name__ == "__main__":
    main()
