from collections import defaultdict
from math import prod

filename = '2020/day1/puzzle.txt'
puzzle_input = open(filename).readlines()
expense_report = [int(i) for i in puzzle_input]

def find_two_that_sum(expense_report, n):
    seen = set()
    for i in expense_report:
        if n-i in seen:
            return (i, n-i)
        else:
            seen.add(i)
    return (0, 0) # no two entries sum to n

def find_three_that_sum(expense_report, n):
    two_way_sums = set()
    two_way_map = defaultdict(set) # maps sum to set of tuples of indices
    for i in range(len(expense_report)):
        for j in range(i, len(expense_report)):
            s = expense_report[i]+expense_report[j]
            two_way_sums.add(s)
            two_way_map[s].add((i, j))
    for k in range(len(expense_report)):
        missing = n - expense_report[k]
        if missing in two_way_sums:
            for tup in two_way_map[missing]:
                if k not in tup:
                    (i, j) = tup
                    return (expense_report[i], expense_report[j], expense_report[k])
    return (0, 0, 0) # no three entries sum to n

def part_1():
    return prod(find_two_that_sum(expense_report, 2020))

def part_2():
    return prod(find_three_that_sum(expense_report, 2020))

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))