import heapq
from typing import Iterable


class Grid:
    def __init__(self):
        self.values = {}
        self.width = 0
        self.height = 0

    @classmethod
    def from_puzzle_input(cls, puzzle_input: list[str]) -> "Grid":
        g = Grid()
        for i, row in enumerate(puzzle_input):
            for j, val in enumerate(row):
                g.set(i, j, val)
        return g

    def repeat(self, n_i: int, n_j: int) -> "Grid":
        """Returns a new Grid consisting of self, repeated n_i times vertically and n_j times horizontally."""
        g = Grid()
        for i in range(self.height * n_i):
            for j in range(self.width * n_j):
                g.set(i, j, self.at(i % self.height, j % self.width))
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
        self.height = max(self.height, i + 1)
        self.width = max(self.width, j + 1)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Grid):
            return False
        return ((self.width == other.width) and (self.height == other.height) and
                (self.values == other.values))

    def where(self, val: str) -> list[tuple[int, int]]:
        return [(i, j) for (i, j), v in self.values.items() if v == val]

    def neighbors(self, point: tuple[int, int], *, allow_wrap_around: bool = False) -> Iterable[tuple[int, int]]:
        """
        allow_wrap_around: If True, wraps the point's coordinates around as if the grid extends to infinity.
        """
        (i, j) = point
        for (di, dj) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            (ni, nj) = (i + di, j + dj)

            if allow_wrap_around:
                (wrapped_ni, wrapped_nj) = (ni % self.height, nj % self.width)
                if self.in_bounds(wrapped_ni, wrapped_nj) and self.at(wrapped_ni, wrapped_nj) != "#":
                    yield (ni, nj)

            else:
                if self.in_bounds(ni, nj) and self.at(ni, nj) != "#":
                    yield (ni, nj)

    def dijkstra(self, start: tuple[int, int]) -> dict[tuple[int, int], int]:
        q = [(0, start)]
        dists = {start: 0}
        visited = set()

        while q:
            dist_so_far, curr = heapq.heappop(q)
            if curr not in visited:
                visited.add(curr)
                for (ni, nj) in self.neighbors(curr):
                    if (ni, nj) not in dists or dists[(ni, nj)] > dist_so_far + 1:
                        dists[(ni, nj)] = dist_so_far + 1
                        heapq.heappush(q, (dist_so_far + 1, (ni, nj)))
        return dists
