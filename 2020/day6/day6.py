from collections import defaultdict

filename = '2020/day6/day6.txt'
puzzle_input = open(filename).readlines()

def get_groups():
    groups = []
    group = ''
    for line in puzzle_input:
        if line == '\n': # break between groups
            groups.append(group.replace('\n', ' ').split())
            group = ''
        else: # continuation of current group
            group += line
    groups.append(group.replace('\n', ' ').split())
    return groups

def get_questions_at_least_one_yes(group):
    return {char for person in group for char in person}

def get_questions_all_yes(group):
    d = defaultdict(int)
    for person in group:
        for char in person:
            d[char] += 1
    return {key for key in d if d[key] == len(group)}

def get_sum_counts(fn):
    return sum([len(fn(group)) for group in get_groups()])

def part_1():
    return get_sum_counts(get_questions_at_least_one_yes)

def part_2():
    return get_sum_counts(get_questions_all_yes)

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))