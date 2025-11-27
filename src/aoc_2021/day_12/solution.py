"""
Advent of Code 2021
Day 12: Passage Pathing
"""

import os
from collections import defaultdict, deque
from pathlib import Path

import click


def get_edges(puzzle_input):
    return {tuple([s.strip() for s in line.split('-')]) for line in puzzle_input}


is_end = lambda s: s == 'end'
is_small = lambda s: s.islower() and not is_end(s)


def get_neighbors(puzzle_input):
    neighbors = defaultdict(set)
    for edge in get_edges(puzzle_input):
        x, y = edge
        if x != 'start':
            neighbors[y].add(x)
        if y != 'start':
            neighbors[x].add(y)
    return neighbors


def cave_generator(puzzle_input, part_2):
    queue = deque()
    start_path = (['start'], 'start', set(), None)
    queue.append(start_path)
    neighbors = get_neighbors(puzzle_input)

    while queue:
        path, most_recent, small_caves_visited, small_cave_visited_twice = queue.popleft()

        for neighbor in neighbors[most_recent]:
            new_path = path + [neighbor]
            if is_end(neighbor):
                yield new_path
            elif is_small(neighbor):
                new_small_caves_visited = small_caves_visited.union({neighbor})
                if part_2:
                    if small_cave_visited_twice is None:
                        new_small_cave_visited_twice = neighbor if neighbor in small_caves_visited else None
                        queue.append((new_path, neighbor, new_small_caves_visited, new_small_cave_visited_twice))
                    elif neighbor != small_cave_visited_twice and neighbor not in small_caves_visited:
                        queue.append((new_path, neighbor, new_small_caves_visited, small_cave_visited_twice))
                elif neighbor not in small_caves_visited:
                    queue.append((new_path, neighbor, new_small_caves_visited, None))
            else:
                queue.append((new_path, neighbor, small_caves_visited, small_cave_visited_twice))


def solve_part_1(puzzle_input: list[str]):
    return len(list(cave_generator(puzzle_input, False)))


def solve_part_2(puzzle_input: list[str]):
    return len(list(cave_generator(puzzle_input, True)))


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
