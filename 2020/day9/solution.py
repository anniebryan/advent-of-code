from collections import deque

filename = '2020/day9/puzzle.txt'
puzzle_input = open(filename).readlines()
numbers = [int(n) for n in puzzle_input]

def init_preamble(consider_prev):
    last_numbers = deque()
    for i in range(consider_prev):
        last_numbers.append(numbers[i])
    return last_numbers, numbers[consider_prev+1:]

def exists_sum(last_numbers, n):
    seen = set()
    for i in last_numbers:
        if n-i in seen:
            return True
        else:
            seen.add(i)
    return False

def find_first_invalid(consider_prev):
    last_numbers, remaining = init_preamble(consider_prev)
    while exists_sum(last_numbers, remaining[0]):
        last_numbers.popleft()
        last_numbers.append(remaining[0])
        remaining = remaining[1:]
    return remaining[0]

def contiguous_sequence(target):
    sequence = deque()
    current_sum = 0
    i = 0
    while current_sum != target:
        if current_sum < target:
            n = numbers[i]
            i += 1
            sequence.append(n)
            current_sum += n
        else: # current sum > target
            n = sequence.popleft()
            current_sum -= n
    return sequence

def encryption_weakness(target):
    sequence = contiguous_sequence(target)
    return max(sequence) + min(sequence)

def part_1():
    return find_first_invalid(25)

def part_2():
    return encryption_weakness(part_1())

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))