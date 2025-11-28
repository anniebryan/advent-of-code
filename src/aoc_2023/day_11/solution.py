"""
Advent of Code 2023
Day 11: Cosmic Expansion
"""

class Loc:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @classmethod
    def dist(cls, loc_a: "Loc", loc_b: "Loc") -> int:
        # manhattan distance
        return abs(loc_a.x - loc_b.x) + abs(loc_a.y - loc_b.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __lt__(self, other: "Loc") -> bool:
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x


def parse_input(puzzle_input: list[str], part_2: bool) -> set[Loc]:
    NUM_TIMES_LARGER = 1000000 if part_2 else 2

    # map from puzzle index of non-empty row -> expanded row index
    row_map = {}
    empty_rows = 0
    for i in range(len(puzzle_input)):
        if set(puzzle_input[i]) == {"."}:
            empty_rows += 1
        else:
            row_map[i] = i + empty_rows * (NUM_TIMES_LARGER - 1)

    # map from puzzle index of non-empty col -> expanded col index
    col_map = {}
    empty_cols = 0
    for j in range(len(puzzle_input[0])):
        if set([row[j] for row in puzzle_input]) == {"."}:
            empty_cols += 1
        else:
            col_map[j] = j + empty_cols * (NUM_TIMES_LARGER - 1)

    # set of all (i, j) galaxy locations in the expanded space
    galaxy_locs = set()
    for i, row in enumerate(puzzle_input):
        for j, ch in enumerate(row):
            if ch == "#":
                galaxy_locs.add(Loc(row_map[i], col_map[j]))
    return galaxy_locs


def all_pairs_shortest_paths(galaxy_locs: set[Loc]) -> dict[tuple[Loc, Loc], int]:
    all_dists = {}
    for loc_a in galaxy_locs:
        for loc_b in galaxy_locs:
            if loc_a < loc_b:
                all_dists[loc_a, loc_b] = Loc.dist(loc_a, loc_b)
    return all_dists


def solve_part_1(puzzle_input: list[str]):
    galaxy_locs = parse_input(puzzle_input, False)
    return sum(all_pairs_shortest_paths(galaxy_locs).values())


def solve_part_2(puzzle_input: list[str]):
    galaxy_locs = parse_input(puzzle_input, True)
    return sum(all_pairs_shortest_paths(galaxy_locs).values())
