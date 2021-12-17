def prod(values):
    prod = 1
    for v in values:
        prod *= v
    return prod


class BitString:
    def __init__(self, hexdata):
        self.bits = bin(int(hexdata, 16))[2:].zfill(len(hexdata) * 4)
        self.offset = 0

    def read_bits(self, n):
        start = self.offset
        self.offset += n
        return self.bits[start:self.offset]

    def read_int(self, n):
        return int(self.read_bits(n), 2)

    def process_packet(self):
        version, typeID = self.read_int(3), self.read_int(3)
        if typeID == 4:
            return version, self.read_literal_packet()
        else:
            version_inner, value = self.process_operator_packet(typeID)
            return version + version_inner, value

    def read_literal_packet(self):
        binary = ""
        while True:
            final_chunk = self.read_int(1) == 0
            binary += self.read_bits(4)
            if final_chunk:
                break
        return int(binary, 2)

    operators = {
        0: sum,
        1: prod,
        2: min,
        3: max,
        5: lambda values: 1 if values[0] > values[1] else 0,
        6: lambda values: 1 if values[0] < values[1] else 0,
        7: lambda values: 1 if values[0] == values[1] else 0,
    }

    def process_operator_packet(self, typeID):
        mode = self.read_int(1)
        if mode == 0:
            version_sum, values = self.process_subpackets_by_size(self.read_int(15))
        else:
            version_sum, values = self.process_n_subpackets(self.read_int(11))
        return version_sum, BitString.operators[typeID](values)

    def process_subpackets_by_size(self, size):
        stop_at = self.offset + size
        version_sum = 0
        values = []
        while self.offset < stop_at:
            version, value = self.process_packet()
            version_sum += version
            values.append(value)
        return version_sum, values

    def process_n_subpackets(self, n):
        version_sum = 0
        values = []
        for _ in range(n):
            version, value = self.process_packet()
            version_sum += version
            values.append(value)
        return version_sum, values


if __name__ == "__main__":
    for line in open("bits.example").read().split():
        print(line, BitString(line).process_packet())
