# The monad program consists of 14 very similar subprograms that each process one input digit.
# z is modified by each subprogram in one of two ways
#   1.) z is multiplied by 26 and a value < 26 is added to z
#   2.) z is divided by 26.  For an invalid model number, z is modified further.
# There are 7 subprograms of each type.  When running all subprograms using a valid model number as
# input, z will be 0 at the end of the full program.
#
# The subprograms have an identical sequence of commands and differ only in 3 numerical arguments
# given to these commands.  One of these is the "div z 26" command found in type 2 programs only -
# type 1 programs have a "div z 1" command there which has no effect.  The "add y <value>" statements
# (line 16 of each subprogram) are effective only for type 1 programs.  The <value> in these
# statements is always positive and will be referred to as p1 (parameter 1) from now.
# Conversely, the "add x <value>" statement (line 6 of each subprogram) is only effective in type 2
# programs.  The <value> here is negative or zero and will be referred to as p2.
#
# The following condition needs to be satisfied for every type 2 subprogram
# (z % 26) + p2 == <input digit>
# In every type 1 subprogram, the value added to z (after multiplying by 26) is p1 + <input digit>
# Combining this, we find this condition for a sequence of a type 1 and type 2 program:
# p1 + <input digit 1> + p2 == <input digit 2>
#
# Not all pairs of type 1 and type 2 programs are immediately adjacent.  This is where the
# multiplication or division by 26 matters:  The value of z is shifted around such that matching
# pairs of subprograms operate on the same "part" of z (e.g. digits in base 26).
#
# Since all input digits must be in [1,9], we can then quickly derive the largest or smallest
# permissible digits (this can even be done with pen & paper).

class Monad:
  def __init__(self, codefile):
    self.program = Monad.build(Monad.load(codefile))


  def load(codefile):
    return open(codefile).read().split("inp w\n")[1:]


  def build(source):
    return [Monad.extract_params(line) for line in source]


  def extract_params(subprogram_code):
    tokens = subprogram_code.split()
    return tuple(int(tokens[statement * 3 + 2]) for statement in [4, 14])


  def find_conditions(self):
    stack = []
    conditions = []
    for index, subprogram in enumerate(self.program):
      p1, p2 = subprogram
      if p1 <= 0:
        index_1, p2_1 = stack.pop()
        index_2, p1_2 = index, p1
        conditions.append((index_2, index_1, p2_1 + p1_2))
      else:
        stack.append((index, p2))
    return conditions


  def find_highest(conditions):
    digits = [9] * 14
    for index_2, index_1, delta in conditions:
      # condition: digit[index_2] == digit[index_1] + delta
      if delta > 0:
        digits[index_1] = 9 - delta
      else:
        digits[index_2] = 9 + delta
    return int("".join(str(digit) for digit in digits))


  def find_lowest(conditions):
    digits = [1] * 14
    for index_2, index_1, delta in conditions:
      # condition: digit[index_2] == digit[index_1] + delta
      if delta > 0:
        digits[index_2] = 1 + delta
      else:
        digits[index_1] = 1 - delta
    return int("".join(str(digit) for digit in digits))


if __name__ == "__main__":
  monad = Monad("monad.input")
  conditions = monad.find_conditions()
  print("Highest model number:", Monad.find_highest(conditions))
  print("Lowest model number: ", Monad.find_lowest(conditions))
