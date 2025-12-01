"""Module defining a Shape class with a method to compute interior points."""

from collections import deque


class Shape:
    def __init__(self, perimeter: set[tuple[int, int]]):
        """Initializes a Shape with the given set of perimeter points."""
        self.perimeter = perimeter

    def get_interior_points(self, exclude_perimeter: bool = False) -> set[tuple[int, int]]:
        """Returns the set of interior points of the shape."""
        x_values = [x for x, _ in self.perimeter]
        y_values = [y for _, y in self.perimeter]
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)

        # TODO: Determine starting point more robustly
        start = (1, 1)
        assert start not in self.perimeter

        interior_points = self.perimeter.copy()
        q: deque[tuple[int, int]] = deque([start])

        while q:
            (x, y) = q.popleft()
            if (x, y) in interior_points:
                continue
            if x < min_x or x > max_x or y < min_y or y > max_y:
                continue
            interior_points.add((x, y))
            for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if neighbor not in interior_points:
                    q.append(neighbor)

        if exclude_perimeter:
            interior_points -= self.perimeter

        return interior_points 