import heapq
from collections import defaultdict
from typing import Any


class UndirectedGraph:
    def __init__(self) -> None:
        self.nodes = set()
        self.graph = defaultdict(set)
        self.edges = set()  # stored as (min, max) to avoid duplicates

    def insert_edge(self, x: Any, y: Any) -> None:
        self.nodes.add(x)
        self.nodes.add(y)
        self.graph[x].add(y)
        self.graph[y].add(x)
        self.edges.add((min(x, y), max(x, y)))

    def neighbors(self, x: Any) -> set[Any]:
        return self.graph[x]

    def remove_edge(self, x: Any, y: Any) -> None:
        self.graph[x].remove(y)
        self.graph[y].remove(x)
        self.edges.remove((min(x, y), max(x, y)))

    def _dfs(self, node: Any, visited: set[Any]) -> None:
        visited.add(node)
        for neighbor in self.graph[node]:
            if neighbor not in visited:
                self._dfs(neighbor, visited)

    def num_connected_components(self) -> int:
        visited = set()
        num_components = 0

        for node in self.nodes:
            if node not in visited:
                num_components += 1
                self._dfs(node, visited)

        return num_components

    def connected_component_sizes(self) -> list[int]:
        visited = set()
        component_sizes = []

        for node in self.nodes:
            if node not in visited:
                size_before = len(visited)
                self._dfs(node, visited)
                size_after = len(visited)
                component_sizes.append(size_after - size_before)

        return component_sizes

    def copy(self) -> "UndirectedGraph":
        new_graph = UndirectedGraph()
        new_graph.nodes = self.nodes.copy()
        new_graph.graph = defaultdict(set, {k: v.copy() for k, v in self.graph.items()})
        new_graph.edges = self.edges.copy()
        return new_graph

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

    def shortest_paths_between(self, start: Any, end: Any) -> list[list[Any]]:
        dists = self.dijkstra(start)
        shortest_path_length = dists[end] + 1
        paths = []
        q = [(start, [start])]

        while q:
            curr, path = q.pop(0)
            if curr == end:
                if len(path) == shortest_path_length:
                    paths.append(path)
            else:
                for n in self.neighbors(curr):
                    if n not in path and len(path) < shortest_path_length:
                        q.append((n, path + [n]))
        return paths
