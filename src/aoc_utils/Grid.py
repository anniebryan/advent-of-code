import heapq


class Grid:
    def __init__(self):
        self.values = {}
        self.width = 0
        self.height = 0

    @classmethod
    def from_puzzle_input(cls, puzzle_input: list[str]) -> "Grid":
        g = Grid()
        g.width = len(puzzle_input[0])
        g.height = len(puzzle_input)
        for i, row in enumerate(puzzle_input):
            for j, val in enumerate(row):
                g.set(i, j, val)
        return g

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

    def dijkstra(self, start: tuple[int, int]) -> dict[tuple[int, int], int]:
        q = [(0, start)]
        dists = {start: 0}
        visited = set()

        while q:
            dist_so_far, curr = heapq.heappop(q)
            if curr not in visited:
                visited.add(curr)
                (i, j) = curr
                for (ni, nj) in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                    if self.in_bounds(ni, nj) and self.at(ni, nj) != "#":
                        if (ni, nj) not in dists or dists[(ni, nj)] > dist_so_far + 1:
                            dists[(ni, nj)] = dist_so_far + 1
                            heapq.heappush(q, (dist_so_far + 1, (ni, nj)))
        return dists
