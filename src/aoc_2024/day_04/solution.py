"""
Advent of Code 2024
Day 4
"""

def parse_input(puzzle_input: list[str]):
    graph = {}
    for i, row in enumerate(puzzle_input):
        for j, ch in enumerate(row):
            graph[(i, j)] = ch
    return graph


def solve_part_1(puzzle_input: list[str]):
    graph = parse_input(puzzle_input, False)
    valid_words = {"XMAS", "SAMX"}
    num_xmas = 0
    for i in range(len(puzzle_input)):
        for j in range(len(puzzle_input[i]) - 3):
            word = "".join([graph[(i, j + x)] for x in range(4)])
            num_xmas += (word in valid_words)
    for i in range(len(puzzle_input) - 3):
        for j in range(len(puzzle_input[i])):
            word = "".join([graph[(i + x, j)] for x in range(4)])
            num_xmas += (word in valid_words)
    for i in range(len(puzzle_input) - 3):
        for j in range(len(puzzle_input[i]) - 3):
            word = "".join([graph[(i + x, j + x)] for x in range(4)])
            num_xmas += (word in valid_words)
    for i in range(3, len(puzzle_input)):
        for j in range(len(puzzle_input[i]) - 3):
            word = "".join([graph[(i - x, j + x)] for x in range(4)])
            num_xmas += (word in valid_words)
    return num_xmas


def solve_part_2(puzzle_input: list[str]):
    graph = parse_input(puzzle_input, True)
    valid_words = {"MAS", "SAM"}
    num_xmas = 0
    for i in range(len(puzzle_input) - 2):
        for j in range(len(puzzle_input) - 2):
            word_1 = "".join([graph[(i + x, j + x)] for x in range(3)])
            word_2 = "".join([graph[(i + 2 - x, j + x)] for x in range(3)])
            num_xmas += (word_1 in valid_words and word_2 in valid_words)
    return num_xmas
