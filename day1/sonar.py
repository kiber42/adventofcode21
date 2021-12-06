def num_increased(depths, step):
    return sum(depths[i] > depths[i - step] for i in range(step, len(depths)))

depths = [int(n) for n in open("sonar.example").readlines()]
print("Number of depth increases:", num_increased(depths, 1))
print("Number of depth increases \"averaged\":", num_increased(depths, 3))
