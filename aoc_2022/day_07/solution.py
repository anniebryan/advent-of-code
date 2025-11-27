"""
Advent of Code 2022
Day 7: No Space Left On Device
"""

import os
from pathlib import Path

import click


# TODO move to utils
class File:
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)


# TODO move to utils
class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.contents = []

    def add_directory(self, directory_name):
        new_directory = Directory(directory_name, self)
        self.contents.append(new_directory)

    def add_file(self, file_name, file_size):
        new_file = File(file_name, file_size)
        self.contents.append(new_file)

    def total_size(self):
        size = 0
        for child in self.contents:
            if isinstance(child, File):
                size += child.size
            else:
                size += child.total_size()
        return size

    def has_child_directory(self, directory_name):
        for child in self.contents:
            if isinstance(child, Directory) and child.name == directory_name:
                return True
        return False

    def get_child_directory(self, directory_name):
        for child in self.contents:
            if isinstance(child, Directory) and child.name == directory_name:
                return child


def stringify(directory, level=0):
    print("     " * level + f"- {directory.name} (dir, total size={directory.total_size()})")
    for child in directory.contents:
        if isinstance(child, File):
            print("     " * (level + 1) + f"- {child.name} (file, size={child.size})")
        else:
            stringify(child, level + 1)


def get_filesystem(puzzle_input):
    root_directory = Directory("/", None)
    current_directory = root_directory
    listing_files = False
    for row in puzzle_input[1:]:
        args = row.split(" ")
        if args[0] == "$":  # is a command
            command = args[1]
            if command == "cd":  # change directory
                directory_name = args[2]
                if directory_name == "..":  # move to parent
                    current_directory = current_directory.parent
                else:
                    assert(current_directory.has_child_directory(directory_name))
                    current_directory = current_directory.get_child_directory(directory_name)
            elif command == "ls":  # list contents
                listing_files = True
            else:
                print(f"unknown command: {command} not in cd, ls")
        else:
            assert(listing_files)
            if args[0] == "dir":
                directory_name = args[1]
                current_directory.add_directory(directory_name)
            else:
                file_size = args[0]
                file_name = args[1]
                current_directory.add_file(file_name, file_size)
    return root_directory


def all_directory_sizes(directory):
    yield directory.total_size()
    for child in directory.contents:
        if isinstance(child, Directory):
            yield from all_directory_sizes(child)


def remaining_space_needed(directory, disk_space, total_needed):
    return directory.total_size() - (disk_space - total_needed)


def solve_part_1(puzzle_input: list[str]):
    filesystem = get_filesystem(puzzle_input)
    max_size = 100000
    return sum([s for s in all_directory_sizes(filesystem) if s <= max_size])


def solve_part_2(puzzle_input: list[str]):
    filesystem = get_filesystem(puzzle_input)
    disk_space = 70000000
    space_needed = 30000000
    total_space_occupied = filesystem.total_size()
    return min([s for s in all_directory_sizes(filesystem) if total_space_occupied - s <= disk_space - space_needed])


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
