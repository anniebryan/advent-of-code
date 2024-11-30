def process_input(puzzle_input):
    numbers = puzzle_input[0].split(",")
    history = {int(n): i+1 for i, n in enumerate(numbers)}
    last_turn = int(numbers[-1])
    i = len(numbers) + 1
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

def nth_number_spoken(puzzle_input, n):
    history, last_turn, i = process_input(puzzle_input)
    while i <= n:
        history, last_turn, i = take_turn(history, last_turn, i)
    return last_turn

def part_1(puzzle_input):
    return nth_number_spoken(puzzle_input, 2020)

def part_2(puzzle_input):
    return nth_number_spoken(puzzle_input, 30000000)
