from copy import deepcopy


class SnailNode:
    def __init__(self, content):
        self.left = SnailNode(content[0]) if isinstance(content[0],
                                                        list) else content[0]
        self.right = SnailNode(content[1]) if isinstance(content[1],
                                                         list) else content[1]

    def __iter__(self):
        for item in SnailNode.iter_helper(self.left, 0, False):
            yield item
        for item in SnailNode.iter_helper(self.right, 1, False):
            yield item

    def __reversed__(self):
        for item in SnailNode.iter_helper(self.right, 1, True):
            yield item
        for item in SnailNode.iter_helper(self.left, 0, True):
            yield item

    def iter_helper(side, prefix, reverse=False):
        if isinstance(side, SnailNode):
            if reverse:
                for item, index in reversed(side):
                    yield item, (prefix, ) + index
            else:
                for item, index in side:
                    yield item, (prefix, ) + index
        else:
            yield side, (prefix, )

    def replace(self, index, value):
        if len(index) > 1:
            if index[0] == 0:
                self.left.replace(index[1:], value)
            else:
                self.right.replace(index[1:], value)
        else:
            if index[0] == 0:
                self.left = value
            else:
                self.right = value

    def magnitude(self):
        m_left = 3 * (self.left.magnitude() if isinstance(
            self.left, SnailNode) else self.left)
        m_right = 2 * (self.right.magnitude() if isinstance(
            self.right, SnailNode) else self.right)
        return m_left + m_right


class SnailNumber:
    def __init__(self, number):
        self.root = SnailNode(number)

    def __iter__(self):
        return iter(self.root)

    def __reversed__(self):
        return reversed(self.root)

    def __str__(self):
        return " ".join(str(item) for item, _ in self)

    def print(self):
        for item in self:
            print(item)

    def iterate_from(self, index0, move_left=False):
        active = False
        iterator = iter(self) if not move_left else reversed(self)
        for item, index in iterator:
            if active:
                yield item, index
            elif index == index0:
                # do not include requested index in output
                active = True

    def replace(self, index, value):
        self.root.replace(index, value)

    def add(self, other):
        if isinstance(other, SnailNumber):
            other = deepcopy(other)
            self.root = SnailNode([self.root, other.root])
        elif isinstance(other, SnailNode):
            other = deepcopy(other)
            self.root = SnailNode([self.root, other])
        else:
            self.root = SnailNode([self.root, SnailNode(other)])

    def explode(self):
        to_explode_gen = (entry for entry in self if len(entry[1]) > 4)
        to_explode = [next(to_explode_gen, None), next(to_explode_gen, None)]
        if to_explode[0] is None:
            return False
        # Assume that the last two items form a pair at level 4; if numbers are consistently reduced, this must always be the case.
        # We check this by comparing all but the last number of the selected indices.
        assert to_explode[-1][1][:-1] == to_explode[-2][1][:-1]
        for move_left in [False, True]:
            explode_value, explode_index = to_explode.pop()
            target_value, target_index = next(
                (entry
                 for entry in self.iterate_from(explode_index, move_left)),
                (None, None))
            if target_value is not None:
                self.replace(target_index, target_value + explode_value)
        self.replace(explode_index[:-1], 0)
        return True

    def split(self):
        split = next((entry for entry in self
                      if isinstance(entry[0], int) and entry[0] >= 10), None)
        if split is None:
            return False
        self.replace(split[1], SnailNode([split[0] // 2, (split[0] + 1) // 2]))
        return True

    def reduce(self):
        while self.explode() or self.split():
            pass

    def magnitude(self):
        return self.root.magnitude()


if __name__ == "__main__":
    number = None
    numbers = []
    for line in open("snailfish.example").readlines():
        exec("number = " + line.strip())
        numbers.append(number)
    # Part 1
    result = SnailNumber(numbers[0])
    for number in numbers[1:]:
        result.add(number)
        result.reduce()
    print(result, "->", result.magnitude())

    # Part 2
    magnitudes = []
    for a in numbers:
        for b in numbers:
            if a == b:
                continue
            result = SnailNumber(a)
            result.add(b)
            result.reduce()
            magnitudes.append(result.magnitude())
    print(max(magnitudes))
