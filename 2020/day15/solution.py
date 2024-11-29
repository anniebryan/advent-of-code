filename = '2020/day15/day15.txt'
puzzle_input = open(filename).read().split(',')

def process_input():
    history = {int(n): i+1 for i, n in enumerate(puzzle_input[:-1])}
    last_turn = int(puzzle_input[-1])
    i = len(puzzle_input) + 1
    return history, last_turn, i

def take_turn(history, last_turn, i):
    """
    history: dictionary mapping a number to the index of the most recent turn that number was spoken
            (if a number has never been spoken, it will not be a key of the dictionary)
    last_turn: the number most recently spoken
    i: the number corresponding to the current turn
    """
    spoken = i-1 - history[last_turn] if last_turn in history else 0
    history[last_turn] = i-1
    return history, spoken, i+1

def nth_number_spoken(n):
    history, last_turn, i = process_input()
    while i <= n:
        history, last_turn, i = take_turn(history, last_turn, i)
    return last_turn

def part_1():
    return nth_number_spoken(2020)

def part_2():
    return nth_number_spoken(30000000)

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))