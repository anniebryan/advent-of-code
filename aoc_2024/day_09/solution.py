"""
Advent of Code 2024
Day 9: Disk Fragmenter
"""

import click
import os
from pathlib import Path
from collections import deque
from utils import IntRangeSet


def parse_input(puzzle_input: list[str], part_2: bool) -> tuple[deque, deque]:
    disk_map_queue = deque()
    is_file = True
    for i, ch in enumerate(puzzle_input[0]):
        if is_file:
            if part_2:
                disk_map_queue.append((int(ch), str(int(i / 2))))
            else:
                for _ in range(int(ch)):
                    disk_map_queue.append(str(int(i / 2)))
        else:
            if part_2:
                disk_map_queue.append((int(ch), "."))
            else:
                for _ in range(int(ch)):
                    disk_map_queue.append(".")
        is_file = not is_file
    return disk_map_queue


def visualize_disk_map(disk_map_queue: deque, part_2: bool) -> str:
    disk_map_queue = disk_map_queue.copy()
    s = []
    while disk_map_queue:
        if part_2:
            (length, file_id) = disk_map_queue.popleft()
            for _ in range(length):
                s.append(file_id)
        else:
            file_id = disk_map_queue.popleft()
            s.append(file_id)
    return "".join(s)


def visualize_ix_to_file_id(ix_to_file_id: dict, total_len: int) -> str:
    s = []
    for i in range(total_len):
        if i in ix_to_file_id:
            s.append(ix_to_file_id[i])
        else:
            s.append(".")
    return "".join(s)


def move_file_blocks_part_1(disk_map_queue: deque) -> deque:
    disk_map_stack = disk_map_queue.copy()
    res = deque()
    while disk_map_stack:
        file_id = disk_map_queue.popleft()
        disk_map_stack.popleft()
        if file_id == ".":
            if not disk_map_stack:
                break
            end_file_id = disk_map_stack.pop()
            while end_file_id == ".":
                if not disk_map_stack:
                    break
                end_file_id = disk_map_stack.pop()
            res.append(end_file_id)
        else:
            res.append(file_id)
    return res


def move_file_blocks_part_2(disk_map_queue: deque) -> deque:
    ix_to_file_id = {}
    empty_ranges = IntRangeSet()
    stack_to_insert = deque()

    i = 0
    while disk_map_queue:
        (length, file_id) = disk_map_queue.popleft()
        if file_id == ".":
            empty_ranges.add_range(i, length - 1)
        else:
            stack_to_insert.append((i, length, file_id))
            for j in range(length):
                ix_to_file_id[i + j] = file_id
        i += length
    total_len = i

    while stack_to_insert:
        (start_ix, ins_length, ins_file_id) = stack_to_insert.pop()
        ix = empty_ranges.min_val_with_length(ins_length - 1)
        if ix is not None and ix < start_ix:
            empty_ranges.remove_range(ix, ins_length - 1)
            for j in range(ins_length):
                ix_to_file_id[ix + j] = ins_file_id
                del ix_to_file_id[start_ix + j]

    res_queue = deque()
    for ix in range(total_len):
        if ix in ix_to_file_id:
            res_queue.append(ix_to_file_id[ix])
        else:
            res_queue.append(".")
    return res_queue


def calc_checksum(res: deque) -> int:
    tot, ix = 0, 0
    while res:
        file_id = res.popleft()
        if file_id != ".":
            tot += ix * int(file_id)
        ix += 1
    return tot


def solve_part_1(puzzle_input: list[str]):
    disk_map_queue = parse_input(puzzle_input, False)
    res = move_file_blocks_part_1(disk_map_queue)
    return calc_checksum(res)


def solve_part_2(puzzle_input: list[str]):
    disk_map_queue= parse_input(puzzle_input, True)
    res = move_file_blocks_part_2(disk_map_queue)
    return calc_checksum(res)


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
