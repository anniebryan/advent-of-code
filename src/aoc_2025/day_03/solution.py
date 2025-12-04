"""
Advent of Code 2025
Day 3: Lobby
"""

def parse_input(puzzle_input: list[str], part_2: bool):
    banks = [[int(n) for n in line] for line in puzzle_input]
    return banks


def _get_max_voltage(bank: list[int], num_digits: int) -> int:
    if num_digits == 1:
        return max(bank)
    max_num = max(bank)
    i = bank.index(max_num)
    if i >= len(bank) - num_digits + 1:
        num_digits_after_i = len(bank) - i - 1
        max_voltage_before_i = _get_max_voltage(bank[:i], num_digits - num_digits_after_i - 1)
        max_voltage = max_voltage_before_i * (10 ** (num_digits_after_i + 1))
        for j, n in enumerate(bank[i:]):
            max_voltage += n * (10 ** (num_digits_after_i - j))
        return max_voltage
    else:
        return max_num * (10 ** (num_digits - 1)) + _get_max_voltage(bank[i + 1:], num_digits - 1)


def solve_part_1(puzzle_input: list[str]):
    banks = parse_input(puzzle_input, False)
    total_max_voltage = 0
    for bank in banks:
        total_max_voltage += _get_max_voltage(bank, 2)
    return total_max_voltage


def solve_part_2(puzzle_input: list[str]):
    banks = parse_input(puzzle_input, True)
    total_max_voltage = 0
    for bank in banks:
        v =  _get_max_voltage(bank, 12)
        total_max_voltage += v
    return total_max_voltage
