"""
Advent of Code 2017
Day 15: Dueling Generators
"""

FACTOR_A = 16807
FACTOR_B = 48271
DIVISOR = 2147483647
NUM_PAIRS_PART_1 = 40_000_000
NUM_PAIRS_PART_2 = 5_000_000


def parse_input(puzzle_input: list[str], part_2: bool):
    a = int(puzzle_input[0].removeprefix("Generator A starts with "))
    b = int(puzzle_input[1].removeprefix("Generator B starts with "))
    return (a, b)


def generator_a(prev_a: int, part_2: bool) -> int:
    a = (prev_a * FACTOR_A) % DIVISOR
    if not part_2:
        return a
    while a % 4 != 0:
        prev_a = a
        a = (prev_a * FACTOR_A) % DIVISOR
    return a


def generator_b(prev_b: int, part_2: bool) -> int:
    b = (prev_b * FACTOR_B) % DIVISOR
    if not part_2:
        return b
    while b % 8 != 0:
        prev_b = b
        b = (prev_b * FACTOR_B) % DIVISOR
    return b


def same_lower_16_bits(a: int, b: int) -> bool:
    return (a % (2 ** 16)) == (b % (2 ** 16))


def solve_part_1(puzzle_input: list[str]):
    a, b = parse_input(puzzle_input, False)
    final_count = 0
    for _ in range(NUM_PAIRS_PART_1):
        prev_a, prev_b = a, b
        a = generator_a(prev_a, False)
        b = generator_b(prev_b, False)
        if same_lower_16_bits(a, b):
            final_count += 1
    return final_count


def solve_part_2(puzzle_input: list[str]):
    a, b = parse_input(puzzle_input, True)
    final_count = 0
    for _ in range(NUM_PAIRS_PART_2):
        prev_a, prev_b = a, b
        a = generator_a(prev_a, True)
        b = generator_b(prev_b, True)
        if same_lower_16_bits(a, b):
            final_count += 1
    return final_count
