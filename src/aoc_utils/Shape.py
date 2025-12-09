"""Module defining a Shape class with a method to compute interior points."""

from collections import defaultdict, deque


class Shape:
    def __init__(self):
        self.perimeter_points = set()
        self.interior_points = set()

    def execute_dig_plan(self, dig_plan: list[tuple[str, int]], start: tuple[int, int] = (0, 0)) -> None:
        """Executes the dig plan consisting of steps ([RDLU], num_steps)."""
        last_point = start
        for direction, num_steps in dig_plan:
            x, y = last_point
            dx, dy = {
                "U": (0, -1),
                "D": (0, +1),
                "R": (+1, 0),
                "L": (-1, 0),
            }[direction]
            for i in range(1, num_steps + 1):
                self.perimeter_points.add((x + dx * i, y + dy * i))
                self.interior_points.add((x + dx * i, y + dy * i))
            last_point = (x + dx * num_steps, y + dy * num_steps)

        x_values = [x for x, _ in self.perimeter_points]
        y_values = [y for _, y in self.perimeter_points]
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)

        # TODO: Determine starting point more robustly
        start = (1, 1)
        assert start not in self.perimeter_points
        q = deque()
        q.append(start)

        while q:
            (x, y) = q.popleft()
            if (x, y) in self.interior_points:
                continue
            if x < min_x or x > max_x or y < min_y or y > max_y:
                continue
            self.interior_points.add((x, y))
            for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if neighbor not in self.interior_points:
                    q.append(neighbor)


    def get_num_interior_points(self, exclude_perimeter: bool = False) -> int:
        """Returns the number of interior points in the shape."""
        if exclude_perimeter:
            return len(self.interior_points - self.perimeter_points)
        return len(self.interior_points)
