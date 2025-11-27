import heapq
from collections import defaultdict, deque
from typing import Any


class DirectedGraph:
    def __init__(self):
        self.graph = defaultdict(set)

    def insert_edge(self, x: Any, y: Any):
        self.graph[x].add(y)

    def neighbors(self, x: Any) -> set[Any]:
        return self.graph[x]

    def exact_path_exists(self, vals: list[Any]) -> bool:
        for v1, v2 in zip(vals, vals[1:]):
            if v2 not in self.graph[v1]:
                return False
        return True
    
    def reorder(self, line: list[str]) -> list[str]:
        q = deque()
        for val in line:
            q.append(([val], val, set(line) - {val}))
        while q:
            path, last, remaining = q.popleft()
            if len(remaining) == 0:
                return path
            for r in remaining:
                if r in self.graph[last]:
                    q.append((path + [r], r, remaining - {r}))
        raise ValueError("Could not find a valid order")

    def dijkstra(self, start: Any) -> dict[Any, int]:
        q = [(0, start)]
        dists = {start: 0}
        visited = set()

        while q:
            dist_so_far, curr = heapq.heappop(q)
            if curr not in visited:
                visited.add(curr)
                for n in self.neighbors(curr):
                    if n not in dists or dists[n] > dist_so_far + 1:
                        dists[n] = dist_so_far + 1
                        heapq.heappush(q, (dist_so_far + 1, n))
        return dists
