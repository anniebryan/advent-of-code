"""
Advent of Code 2023
Day 1: Trebuchet?!
"""

DIGIT_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def map_index_to_digit(line: str, part_2: bool) -> dict[int, int]:
    digit_map = {}
    for i, char in enumerate(line):
        if char.isdigit():
            digit_map[i] = int(char)
    if part_2:
        for k, v in DIGIT_WORDS.items():
            for i in range(len(line) - len(k) + 1):
                if line[i:i + len(k)] == k:
                    digit_map[i] = v
    return digit_map


def get_calibration_value(line: str, part_2: bool) -> int:
    digit_map = map_index_to_digit(line, part_2)
    min_ix, max_ix = min(digit_map), max(digit_map)
    first_digit, last_digit = digit_map[min_ix], digit_map[max_ix]
    return int(f"{first_digit}{last_digit}")


def get_all_calibration_values(puzzle_input: list[str], part_2: bool) -> list[int]:
    calibration_values = []
    for line in puzzle_input:
        calibration_values.append(get_calibration_value(line, part_2))
    return calibration_values


def part_1(puzzle_input: list[str]) -> int:
    if puzzle_input[0] == "part 2 only":
        return "Not supported"
    return sum(get_all_calibration_values(puzzle_input[1:], False))


def part_2(puzzle_input: list[str]) -> int:
    if puzzle_input[0] == "part 1 only":
        return "Not supported"
    return sum(get_all_calibration_values(puzzle_input[1:], True))
