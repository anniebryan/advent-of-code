from collections import defaultdict, deque

class DirectedGraph:
    def __init__(self):
        self.graph = defaultdict(set)

    def insert_edge(self, x: int, y: int):
        self.graph[x].add(y)

    def exact_path_exists(self, nums: list[int]) -> bool:
        for n1, n2 in zip(nums, nums[1:]):
            if n2 not in self.graph[n1]:
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