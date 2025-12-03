"""
Advent of Code 2025
Day 3: Lobby
"""

def parse_input(puzzle_input: list[str], part_2: bool):
    banks = [[int(n) for n in line] for line in puzzle_input]
    return banks


def solve_part_1(puzzle_input: list[str]):
    banks = parse_input(puzzle_input, False)
    total_max_voltage = 0
    for bank in banks:
        max_num = max(bank)
        i = bank.index(max_num)
        if i == len(bank) - 1:
            second_max_num = max(bank[:-1])
            total_max_voltage += second_max_num * 10 + max_num
        else:
            second_max_num = max(bank[i + 1:])
            total_max_voltage += max_num * 10 + second_max_num
    return total_max_voltage


def solve_part_2(puzzle_input: list[str]):
    _ = parse_input(puzzle_input, True)
    return
