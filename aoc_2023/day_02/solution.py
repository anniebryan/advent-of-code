"""
Advent of Code 2023
Day 2: Cube Conundrum
"""

import click
import os
import pathlib
import regex as re


def parse_input(puzzle_input: list[str]) -> dict[int, list[dict[str, int]]]:
    pattern = r'Game (?P<game_id>\d+): (?P<sets>.*)'
    game_map = {}
    for line in puzzle_input:
        match = re.match(pattern, line)
        game_id = match.group('game_id')
        game_records = []
        for game_set in match.group('sets').split("; "):
            game_record = {}
            for cubes in game_set.split(", "):
                number, color = cubes.split(" ")
                game_record[color] = int(number)
            game_records.append(game_record)
        game_map[int(game_id)] = game_records
    return game_map


def is_game_possible(game_records: list[dict[str, int]], red_cubes: int, green_cubes: int, blue_cubes: int) -> bool:
    for game_record in game_records:
        if game_record.get('red', 0) > red_cubes:
            return False
        if game_record.get('green', 0) > green_cubes:
            return False
        if game_record.get('blue', 0) > blue_cubes:
            return False
    return True


def determine_min_cubes_needed(game_records: list[dict[str, int]]) -> tuple[int, int, int]:
    max_red_seen, max_green_seen, max_blue_seen = 0, 0, 0
    for game_record in game_records:
        max_red_seen = max(max_red_seen, game_record.get('red', 0))
        max_green_seen = max(max_green_seen, game_record.get('green', 0))
        max_blue_seen = max(max_blue_seen, game_record.get('blue', 0))
    return max_red_seen, max_green_seen, max_blue_seen


def solve_part_1(puzzle_input: list[str]) -> int:
    game_map = parse_input(puzzle_input)
    all_possible_game_ids = []
    for game_id, game_records in game_map.items():
        if is_game_possible(game_records, red_cubes=12, green_cubes=13, blue_cubes=14):
            all_possible_game_ids.append(game_id)
    return sum(all_possible_game_ids)


def solve_part_2(puzzle_input: list[str]) -> int:
    game_map = parse_input(puzzle_input)
    all_powers = []
    for game_records in game_map.values():
        red, green, blue = determine_min_cubes_needed(game_records)
        power = red * green * blue
        all_powers.append(power)
    return sum(all_powers)


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = pathlib.Path(__file__).parent
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
