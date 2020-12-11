from collections import defaultdict

filename = '2020/day10/day10.txt'
puzzle_input = open(filename).readlines()
numbers = [int(n) for n in puzzle_input]

def get_differences(numbers):
    numbers = sorted(numbers + [0, max(numbers) + 3])
    d = defaultdict(int)
    for i in range(len(numbers) - 1):
        d[numbers[i+1] - numbers[i]] += 1
    return d

def num_arrangements(numbers, last, memo={}):
    n = len(numbers)
    if n in {0, 1}: return 1
    if (n, last) not in memo:
        ways = 0
        i = 0
        while i < len(numbers) and numbers[i] <= last + 3:
            ways += num_arrangements(numbers[i+1:], numbers[i])
            i += 1
        memo[(n, last)] = ways
    return memo[(n, last)]

def part_1():
    d = get_differences(numbers)
    return d[1]*d[3]

def part_2():
    return num_arrangements(sorted(numbers), 0)

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))