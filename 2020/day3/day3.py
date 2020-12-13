from math import prod

filename = '2020/day3/day3.txt'
puzzle_input = open(filename).readlines()

def num_trees(right, down):
    width = len([i for i in puzzle_input[0] if i == "." or i == "#"])
    num_trees = 0
    y = 0
    for x in range(len(puzzle_input)):
        if x % down == 0:
            if puzzle_input[x][y] == "#": # tree
                num_trees += 1
            y += right
            y %= width
    return num_trees

def part_1():
    return num_trees(3,1)

def part_2():
    all_ways = [(1,1),(3,1),(5,1),(7,1),(1,2)]
    return prod([num_trees(*way) for way in all_ways])

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))