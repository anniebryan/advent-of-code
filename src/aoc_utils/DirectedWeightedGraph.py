import heapq
from collections import defaultdict
from typing import Any


class DirectedWeightedGraph:
    def __init__(self):
        self.neighbors = defaultdict(set)
        self.weights = {}

    def insert_edge(self, x: Any, y: Any, w: int = 1) -> None:
        self.neighbors[x].add(y)
        self.weights[(x, y)] = w

    def dijkstra(self, start: Any) -> dict[Any, int]:
        q = [(0, start)]
        dists = {start: 0}
        visited = set()

        while q:
            dist_so_far, curr = heapq.heappop(q)
            if curr not in visited:
                visited.add(curr)
                for n in self.neighbors[curr]:
                    w = self.weights[(curr, n)]
                    new_dist = dist_so_far + w
                    if n not in dists or dists[n] > new_dist:
                        dists[n] = new_dist
                        heapq.heappush(q, (new_dist, n))
        return dists
