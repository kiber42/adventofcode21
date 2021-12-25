import numpy as np


def parse_instruction(line):
    cmd, pos = line.strip().split(" ")
    cmd = 1 if cmd == "on" else 0
    ranges = pos.split(",")
    coords = tuple(int(val) for range in ranges for val in range[2:].split(".."))
    return cmd, coords

def init(filename):
    boot_map = np.zeros((101, 101, 101))
    for line in open(filename).readlines():
        cmd, coords = parse_instruction(line)
        rx0, rx1, ry0, ry1, rz0, rz1 = coords
        if min(coords) < -50 or max(coords) > 50:
            continue
        for x in range(rx0 + 50, rx1 + 51):
            for y in range(ry0 + 50, ry1 + 51):
                for z in range(rz0 + 50, rz1 + 51):
                    boot_map[x, y, z] = cmd
    print(sum(sum(sum(boot_map == 1))))


class Cuboid:
    def __init__(self, line, cmd=None, coords=None):
        if line is not None:
            self.cmd, self.coords = parse_instruction(line)
        else:
            self.cmd, self.coords = cmd, coords

    def __str__(self):
        return "x={}..{},y={}..{},z={}..{}, cmd={}".format(*self.coords, self.cmd)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.coords == other.coords

    def volume(self):
        return (self.coords[1] - self.coords[0] + 1) * (self.coords[3] - self.coords[2] + 1) * (self.coords[5] - self.coords[4] + 1)

    def overlap(self, other):
        if (self.coords[0] > other.coords[1] or self.coords[2] > other.coords[3] or self.coords[4] > other.coords[5] or
                other.coords[0] > self.coords[1] or other.coords[2] > self.coords[3] or other.coords[4] > self.coords[5]):
            return None
        return Cuboid(None, other.cmd, (
            max(self.coords[0], other.coords[0]), min(self.coords[1], other.coords[1]),
            max(self.coords[2], other.coords[2]), min(self.coords[3], other.coords[3]),
            max(self.coords[4], other.coords[4]), min(self.coords[5], other.coords[5])))


# pos has to be "non-integral" (e.g 0.5 to split between 0 and 1)
def split_x(cuboids, pos):
    output = []
    for cuboid in cuboids:
        c = cuboid.coords
        if pos > c[0] and pos < c[1]:
            output.append(
                Cuboid(None, cuboid.cmd, (c[0], (int)(pos - 0.5), c[2], c[3], c[4], c[5])))
            output.append(
                Cuboid(None, cuboid.cmd, ((int)(pos + 0.5), c[1], c[2], c[3], c[4], c[5])))
        else:
            output.append(cuboid)
    return output


def split_y(cuboids, pos):
    output = []
    for cuboid in cuboids:
        c = cuboid.coords
        if pos > c[2] and pos < c[3]:
            output.append(
                Cuboid(None, cuboid.cmd, (c[0], c[1], c[2], (int)(pos - 0.5), c[4], c[5])))
            output.append(
                Cuboid(None, cuboid.cmd, (c[0], c[1], (int)(pos + 0.5), c[3], c[4], c[5])))
        else:
            output.append(cuboid)
    return output


def split_z(cuboids, pos):
    output = []
    for cuboid in cuboids:
        c = cuboid.coords
        if pos > c[4] and pos < c[5]:
            output.append(
                Cuboid(None, cuboid.cmd, (c[0], c[1], c[2], c[3], c[4], (int)(pos - 0.5))))
            output.append(
                Cuboid(None, cuboid.cmd, (c[0], c[1], c[2], c[3], (int)(pos + 0.5), c[5])))
        else:
            output.append(cuboid)
    return output


def split_from_overlap(cuboid, overlap):
    overlap = overlap.coords
    cuboids = split_x([cuboid], overlap[0] - 0.5)
    cuboids = split_y(cuboids, overlap[2] - 0.5)
    cuboids = split_z(cuboids, overlap[4] - 0.5)
    cuboids = split_x(cuboids, overlap[1] + 0.5)
    cuboids = split_y(cuboids, overlap[3] + 0.5)
    cuboids = split_z(cuboids, overlap[5] + 0.5)
    return cuboids


def reboot(filename):
    # Process cuboids in reverse order. The last entry cannot be overwritten by any other,
    # the second to last only needs to check if it overlaps with the last one, etc.
    cuboids = [Cuboid(line) for line in open(filename).readlines()]
    final = [cuboids[-1]]
    for cuboid in reversed(cuboids[:-1]):
        insert_queue = [cuboid]
        while insert_queue:
            to_insert = insert_queue.pop()
            for reference in final:
                overlap = to_insert.overlap(reference)
                if overlap:
                    if overlap != to_insert:
                        insert_queue.extend(
                            split_from_overlap(to_insert, overlap))
                    break
            else:
                # No overlaps, accept cuboid as is
                final.append(to_insert)
    print(sum(cuboid.volume() for cuboid in final if cuboid.cmd == 1))


if __name__ == "__main__":
    init("reactor.example")
    reboot("reactor.example2")
