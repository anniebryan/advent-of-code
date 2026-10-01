"""
Advent of Code 2017
Day 9: Stream Processing
"""

from collections import Counter


def parse_input(puzzle_input: list[str], part_2: bool):
    return puzzle_input[0]


def _remove_exclamations(stream: str) -> str:
    chars = []
    i = 0
    while i < len(stream):
        if stream[i] == "!":
            i += 2
        else:
            chars.append(stream[i])
            i += 1
    return "".join(chars)


def _remove_garbage(stream: str) -> tuple[str, str]:
    chars_to_keep = []
    chars_to_remove = []
    inside_garbage = False
    for ch in stream:
        if ch == "<":
            if inside_garbage:
                chars_to_remove.append(ch)
            inside_garbage = True
        elif ch == ">":
            inside_garbage = False
        elif not inside_garbage:
            chars_to_keep.append(ch)
        else:
            chars_to_remove.append(ch)
    return "".join(chars_to_keep), "".join(chars_to_remove)


def _get_score(stream: str) -> int:
    curr_score = 0
    curr_level = 0
    for ch in stream:
        if ch == "{":
            curr_level += 1
        elif ch == "}":
            curr_score += curr_level
            curr_level -= 1
    assert curr_level == 0
    return curr_score


def solve_part_1(puzzle_input: list[str]):
    stream = parse_input(puzzle_input, False)
    stream = _remove_exclamations(stream)
    stream, _ = _remove_garbage(stream)

    char_counts = Counter(stream)
    num_open_brackets = char_counts["{"]
    num_closed_brackets = char_counts["}"]
    assert num_open_brackets == num_closed_brackets

    return _get_score(stream)


def solve_part_2(puzzle_input: list[str]):
    stream = parse_input(puzzle_input, False)
    stream = _remove_exclamations(stream)
    _, chars_removed = _remove_garbage(stream)
    return len(chars_removed)
