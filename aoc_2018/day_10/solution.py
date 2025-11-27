"""
Advent of Code 2018
Day 10: The Stars Align
"""

import click
import os
from pathlib import Path
import regex as re


def get_data(puzzle_input):
    data = [[int(x) for x in re.findall(r'-?\d+', i)] for i in puzzle_input]
    return data


def get_boxes(data):
    boxes = []
    for i in range(20000):
        minx, maxx, miny, maxy = 10000, 0, 10000, 0
        for row in data:
            x, y, vx, vy = row
            newx = x + i * vx
            newy = y + i * vy
            
            minx = min(minx, newx)
            maxx = max(maxx, newx)
            miny = min(miny, newy)
            maxy = max(maxy, newy)
        boxes.append([maxx, minx, maxy, miny])
    return boxes


def get_box_size(box):
    maxx, minx, maxy, miny = box
    return maxx - minx + maxy - miny


def get_smallest_box(boxes):
    answer_box = min(get_box_size(box) for box in boxes)
    for i, box in enumerate(boxes):
        maxx, minx, maxy, miny = box
        if answer_box == maxx - minx + maxy - miny:
            return i, box


def solve_part_1(puzzle_input: list[str]):
    data = get_data(puzzle_input)
    boxes = get_boxes(data)
    i, box = get_smallest_box(boxes)
    maxx, minx, maxy, miny = box

    grid = [[' '] * (maxx - minx + 1) for j in range(miny, maxy + 1)]
    for (x, y, vx, vy) in data:
        grid[y - miny + i * vy][x - minx + i * vx] = '#'

    output = ["\n"]
    for row in grid:
        output.append(" ".join(row))
    return "\n".join(output)


def solve_part_2(puzzle_input: list[str]):
    data = get_data(puzzle_input)
    boxes = get_boxes(data)
    i, _ = get_smallest_box(boxes)
    return i


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = Path(__file__).parent
    example_files = sorted([fn for fn in os.listdir(base_dir) if fn.endswith(".txt") and "example" in fn])

    def _run_solution(filename: str, display_name: str):
        print(f"--- {display_name} ---")

        if not (filepath := (base_dir / filename)).exists():
            print(f"{filename} not found.")
            return

        with open(filepath) as file:
            puzzle_input = [line.strip("\n") for line in file]
            print(f"Part 1: {solve_part_1(puzzle_input)}")
            print(f"Part 2: {solve_part_2(puzzle_input)}")
        return

    if not skip_example:
        if len(example_files) < 2:
            _run_solution("example.txt", "Example")
        else:
            for i, filename in enumerate(example_files):
                _run_solution(filename, f"Example {i + 1}")

    if not skip_puzzle:
        _run_solution("puzzle.txt", "Puzzle")


if __name__ == "__main__":
    main()
