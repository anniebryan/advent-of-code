"""
Advent of Code 2025
Day 7: Laboratories
"""

from collections import defaultdict


def parse_input(puzzle_input: list[str], part_2: bool):
    assert "S" in puzzle_input[0]
    start_x = puzzle_input[0].index("S")
    
    # row # -> index of splitter
    all_splitters = defaultdict(set)
    for i, row in enumerate(puzzle_input):
        for j, ch in enumerate(row):
            if ch == "^":
                all_splitters[i].add(j)

    return start_x, all_splitters


def solve_part_1(puzzle_input: list[str]):
    start_x, all_splitters = parse_input(puzzle_input, False)
    beams = set([start_x])
    num_splits = 0
    for depth in range(1, max(all_splitters) + 2):
        if (splitters := all_splitters.get(depth)):
            new_beams = set()
            for b in beams:
                if b in splitters:
                    num_splits += 1
                    new_beams.add(b - 1)
                    new_beams.add(b + 1)
                else:
                    new_beams.add(b)
            beams = new_beams
    return num_splits


def solve_part_2(puzzle_input: list[str]):
    start_x, all_splitters = parse_input(puzzle_input, True)
    beams = set([start_x])
    num_paths = defaultdict(int)
    num_paths[start_x] = 1
    for depth in range(1, max(all_splitters) + 2):
        if (splitters := all_splitters.get(depth)):
            new_beams = set()
            new_num_paths = defaultdict(int)
            for b in beams:
                if b in splitters:
                    new_beams.add(b - 1)
                    new_beams.add(b + 1)
                    new_num_paths[b - 1] += num_paths[b]
                    new_num_paths[b + 1] += num_paths[b]
                else:
                    new_beams.add(b)
                    new_num_paths[b] += num_paths[b]
            beams = new_beams
            num_paths = new_num_paths
    return sum(num_paths.values())
