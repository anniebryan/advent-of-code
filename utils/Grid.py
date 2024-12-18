class Grid:
    def __init__(self, puzzle_input: list[str]):
        self.values = {}
        self.width = len(puzzle_input[0])
        self.height = len(puzzle_input)
        for i, row in enumerate(puzzle_input):
            for j, val in enumerate(row):
                self.values[(i, j)] = val

    def at(self, i: int, j: int) -> str:
        return self.values[(i, j)]

    def in_bounds(self, i: int, j: int) -> bool:
        return (i, j) in self.values

    def __iter__(self):
        for (i, j) in sorted(self.values.keys()):
            yield (i, j)

    def __repr__(self):
        output = []
        for i in range(self.height):
            s = []
            for j in range(self.width):
                s.append(str(self.values[(i, j)]))
            output.append("".join(s))
        return "\n".join(output)

    def set(self, i: int, j: int, val: str) -> None:
        self.values[(i, j)] = val

    def __eq__(self, other) -> bool:
        if not isinstance(other, Grid):
            return False
        return ((self.width == other.width) and (self.height == other.height) and
                (self.values == other.values))

    def where(self, val: str) -> list[tuple[int, int]]:
        return [(i, j) for (i, j), v in self.values.items() if v == val]
