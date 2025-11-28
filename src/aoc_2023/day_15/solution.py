"""
Advent of Code 2023
Day 15: Lens Library
"""

from collections import defaultdict, deque


def parse_input(puzzle_input: list[str]):
    for s in puzzle_input[0].split(","):
        yield s


def run_hash_algorithm(s: str) -> int:
    tot = 0
    for ch in s:
        tot += ord(ch)
        tot *= 17
        tot %= 256
    return tot


def get_all_boxes(puzzle_input: list[str]) -> tuple[dict[int, deque], dict[str, str]]:
    all_labels = set()
    focal_lengths = {}
    boxes = defaultdict(deque)
    for s in parse_input(puzzle_input):
        if "-" in s:
            label = s.split("-")[0]
            box = run_hash_algorithm(label)
            if label in all_labels:
                all_labels.remove(label)
                boxes[box].remove(label)
        else:
            label, focal_len = s.split("=")
            box = run_hash_algorithm(label)
            focal_lengths[label] = focal_len
            if label not in all_labels:
                all_labels.add(label)
                boxes[box].append(label)
    return boxes, focal_lengths


def focusing_power(boxes: dict[int, deque], focal_lengths: dict[str, str]) -> None:
    tot = 0
    for box_num, lenses in boxes.items():
        for i, label in enumerate(lenses):
            tot += (box_num + 1) * (i + 1) * int(focal_lengths[label])
    return tot


def solve_part_1(puzzle_input: list[str]):
    return sum([run_hash_algorithm(s) for s in parse_input(puzzle_input)])


def solve_part_2(puzzle_input: list[str]):
    boxes, focal_lengths = get_all_boxes(puzzle_input)
    return focusing_power(boxes, focal_lengths)
