"""
Advent of Code 2025
Day 12: Christmas Tree Farm
"""

import re

import numpy as np


class Present:

    def __init__(self, locs: set[tuple[int, int]]):
        self.locs = locs
        if locs:
            self.height = max(i for i, _ in self.locs) + 1
            self.width = max(j for _, j in self.locs) + 1
        else:
            self.height = 0
            self.width = 0

    @classmethod
    def from_puzzle_input(cls, puzzle_input: list[str]) -> "Present":
        locs = set()
        for i, line in enumerate(puzzle_input):
            for j, ch in enumerate(line):
                if ch == "#":
                    locs.add((i, j))
        return Present(locs)

    def __repr__(self) -> str:
        s = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if (i, j) in self.locs:
                    row.append("#")
                else:
                    row.append(".")
            s.append("".join(row))
        return "\n".join(s)

    def get_rotated_variants(self, num_rotations: int = 1) -> set["Present"]:
        rotations = set()
        p = self
        for _ in range(num_rotations):
            p = Present({(j, p.height - i - 1) for (i, j) in p.locs})
            rotations.add(p)
        return rotations

    def apply_offset(self, i_offset: int, j_offset: int) -> "Present":
        return Present({(i + i_offset, j + j_offset) for (i, j) in self.locs})

    def make_solid(self) -> "Present":
        return Present({(i, j) for i in range(self.height) for j in range(self.width)})


def parse_input(puzzle_input: list[str], part_2: bool):
    presents: dict[int, Present] = {}
    current_ix, current_present = None, None
    for i, line in enumerate(puzzle_input):
        if line == "":
            assert isinstance(current_ix, int)
            assert isinstance(current_present, list)
            presents[current_ix] = Present.from_puzzle_input(current_present)
        elif (match := re.match(r"^(?P<num>\d+):$", line)):
            current_ix = int(match.group("num"))
            current_present = []
        elif re.match(r"^\d+x\d+:.*$", line):
            break
        elif re.match(r"^[\.|#]+$", line):
            assert isinstance(current_present, list)
            current_present.append(line)
        else:
            raise ValueError(f"Unexpected {line=}")

    regions = []
    for line in puzzle_input[i:]:
        match = re.match(r"^(?P<width>\d+)x(?P<length>\d+): (?P<presents>.*)$", line)
        assert match is not None
        width = int(match.group("width"))
        length = int(match.group("length"))
        shapes = [int(p) for p in match.group("presents").split()]
        regions.append((width, length, shapes))

    return presents, regions


def all_presents_can_fit(available_spaces: np.ndarray, shapes_to_fit: list[Present]) -> bool:
    if len(shapes_to_fit) == 0:
        return True

    if sum(len(shape.locs) for shape in shapes_to_fit) > len(available_spaces) * len(available_spaces[0]):
        return False

    s = shapes_to_fit[0]
    for rotated_s in s.get_rotated_variants(4):
        for i_offset in range(len(available_spaces) - rotated_s.height + 1):
            for j_offset in range(len(available_spaces[0]) - rotated_s.width + 1):
                offset_s = rotated_s.apply_offset(i_offset, j_offset)
                if all(available_spaces[i][j] == 1 for (i, j) in offset_s.locs):
                    new_available_spaces = available_spaces.copy()
                    for (i, j) in offset_s.locs:
                        new_available_spaces[i][j] = 0
                    if all_presents_can_fit(new_available_spaces, shapes_to_fit[1:]):
                        return True

    return False


def solve_part_1(puzzle_input: list[str]):
    presents, regions = parse_input(puzzle_input, False)
    result = 0
    for (width, length, shapes) in regions:
        shapes_to_fit: list[Present] = []
        for i, num in enumerate(shapes):
            shapes_to_fit.extend([presents[i]] * num)
        available_spaces = np.array([[1] * width] * length, dtype=int)

        # check if all shapes were solid (#) with no spaces, could they fit
        solid_shapes = [s.make_solid() for s in shapes_to_fit]
        if all_presents_can_fit(available_spaces, solid_shapes):
            result += 1
        elif all_presents_can_fit(available_spaces, shapes_to_fit):
            result += 1
    return result


def solve_part_2(puzzle_input: list[str]):
    return
