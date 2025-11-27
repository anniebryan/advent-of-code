"""
Advent of Code 2021
Day 4: Giant Squid
"""

import click
import os
from pathlib import Path

SIZE = 5

row = lambda marked: any([all([(i, j) in marked for j in range(SIZE)]) for i in range(SIZE)])
col = lambda marked: any([all([(i, j) in marked for i in range(SIZE)]) for j in range(SIZE)])
wins = lambda marked: row(marked) or col(marked)


def get_input_numbers(puzzle_input):
    return [int(n) for n in puzzle_input[0].split(',')]


def get_input_boards(puzzle_input):
    boards = []
    current_board = []
    for row in puzzle_input[2:]:
        if row == "":
            boards.append(current_board)
            current_board = []
        else:
            current_board.append([int(item) for item in row.split() if len(item) > 0])
    boards.append(current_board)

    boards_dict = {}
    for i, board in enumerate(boards):
        board_dict = {}
        for j, row in enumerate(board):
            for k, val in enumerate(row):
                board_dict[val] = (j, k)
        boards_dict[i] = board_dict
    return boards_dict


def solve_part_1(puzzle_input: list[str]):
    input_numbers = get_input_numbers(puzzle_input)
    input_boards = get_input_boards(puzzle_input)
    num_boards = len(input_boards)

    marked_spaces = {i: set() for i in range(num_boards)}
    for num in input_numbers:
        for j in range(num_boards):
            if num in input_boards[j]:
                marked_spaces[j].add(input_boards[j][num])
        has_won = [wins(marked_spaces[i]) for i in range(num_boards)]
        if any(has_won):
            winning_board_num = list(filter(lambda tup: tup[1], [(i, board) for i, board in enumerate(has_won)]))[0][0]
            winning_board = {input_boards[winning_board_num][n]: n for n in input_boards[winning_board_num]}
            all_spaces = {(i,j) for i in range(SIZE) for j in range(SIZE)}
            unmarked = [winning_board[s] for s in all_spaces if s not in marked_spaces[winning_board_num]]
            return sum(unmarked) * num


def solve_part_2(puzzle_input: list[str]):
    input_numbers = get_input_numbers(puzzle_input)
    input_boards = get_input_boards(puzzle_input)
    num_boards = len(input_boards)
    
    marked_spaces = {i: set() for i in range(num_boards)}
    prev_has_won = [wins(marked_spaces[i]) for i in range(num_boards)]
    for num in input_numbers:
        for j in range(num_boards):
            if num in input_boards[j]:
                marked_spaces[j].add(input_boards[j][num])
        has_won = [wins(marked_spaces[i]) for i in range(num_boards)]
        if all(has_won) and not all(prev_has_won):
            winning_board_num = list(filter(lambda tup: not tup[1], [(i, board) for i, board in enumerate(prev_has_won)]))[0][0]
            winning_board = {input_boards[winning_board_num][n]: n for n in input_boards[winning_board_num]}
            all_spaces = {(i,j) for i in range(SIZE) for j in range(SIZE)}
            unmarked = [winning_board[s] for s in all_spaces if s not in marked_spaces[winning_board_num]]
            return sum(unmarked) * num
        else:
            prev_has_won = has_won


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
