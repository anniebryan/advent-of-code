class Grid:
    def __init__(self, puzzle_input: list[str]):
        self.values = {}
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
