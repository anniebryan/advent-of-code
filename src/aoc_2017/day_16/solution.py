"""
Advent of Code 2017
Day 16: Permutation Promenade
"""

NUM_DANCES = 1_000_000_000


def parse_input(puzzle_input: list[str], part_2: bool):
    programs = list(puzzle_input[0])
    moves = puzzle_input[1].split(",")
    return programs, moves


def apply_move(move: str, programs: list[str]) -> list[str]:
    if move.startswith("s"):
        spin_size = int(move.removeprefix("s"))
        programs = programs[-spin_size:] + programs[:-spin_size]
    elif move.startswith("x"):
        a, b = move.removeprefix("x").split("/")
        a, b = int(a), int(b)
        programs[a], programs[b] = programs[b], programs[a]
    elif move.startswith("p"):
        a, b = move.removeprefix("p").split("/")
        a_ix = programs.index(a)
        b_ix = programs.index(b)
        programs[a_ix], programs[b_ix] = programs[b_ix], programs[a_ix]
    else:
        raise ValueError(f"Unexpected {move=}")

    return programs


def solve_part_1(puzzle_input: list[str]):
    programs, moves = parse_input(puzzle_input, False)
    for move in moves:
        programs = apply_move(move, programs)
    return "".join(programs)


def solve_part_2(puzzle_input: list[str]):
    programs, moves = parse_input(puzzle_input, True)
    init_program = "".join(programs)
    seen = {}
    for i in range(NUM_DANCES):
        for move in moves:
            programs = apply_move(move, programs)
        p = "".join(programs)
        if p == init_program:
            break
        seen[i + 1] = p
    cycle_size = i + 1
    return seen.get(NUM_DANCES % cycle_size, "N/A")
