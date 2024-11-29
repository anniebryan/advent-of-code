import re

file = open('2019/day4/puzzle.txt')
given_range = file.readlines()
min_r, max_r = (int(x) for x in re.findall('(\d+)-(\d+)', given_range[0])[0])


def adjacent_digits(n):
    s = str(n)
    adjacent = [s[i] == s[i+1] for i in range(len(s)-1)]
    return any(adjacent)


def never_decreases(n):
    s = str(n)
    decreases = [s[i] > s[i+1] for i in range(len(s)-1)]
    return not any(decreases)


def contains_double(n):
    s = str(n)
    lengths = []
    current = 1
    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            current += 1
        else:
            lengths.append(current)
            current = 1
    lengths.append(current)
    return 2 in lengths


def part_1():
    valid_passwords = [n for n in range(min_r, max_r + 1) if adjacent_digits(n) and never_decreases(n)]
    return len(valid_passwords)


def part_2():
    valid_passwords = [n for n in range(min_r, max_r + 1) if contains_double(n) and never_decreases(n)]
    return(len(valid_passwords))


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
