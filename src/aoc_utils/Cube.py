from collections import defaultdict, deque
from typing import Iterable

from .Grid import Grid


def _neg(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    """Return the vector facing the opposite direction."""
    return tuple(-value for value in vector)  # pyright: ignore[reportReturnType]


class CubeFace:
    """
    Represents one face of a Cube, with values stored in a dictionary mapping (i, j) coordinates to strings.

    The (i, j) coordinates are relative to the face when viewed according to the layout in the Cube docstring,
    starting from (0, 0) at the top-left corner.

    (0, 0)  (0, 1)  (0, 2) ...
    (1, 0)  (1, 1)  (1, 2) ...
    (2, 0)  (2, 1)  (2, 2) ...
    ...

    """
    def __init__(self, face_id: int, values: dict[tuple[int, int], str]):
        self.id = face_id
        self.values = values

    def at(self, row: int, col: int) -> str:
        return self.values[row, col]


class Cube:
    """
    Represents a cube made of 6 CubeFaces, with IDs 1-6 in the following layout.

            +---+
            | 1 |
        +---+---+---+
        | 2 | 3 | 4 |
        +---+---+---+
            | 5 |
            +---+
            | 6 |
            +---+
    """

    DIRS: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(
        self,
        face_size: int,
        faces: dict[int, CubeFace],
        face_positions: dict[int, tuple[int, int]],
        orientations: dict[
            int,
            tuple[
                tuple[int, int, int],
                tuple[int, int, int],
                tuple[int, int, int],
            ],
        ],
    ):
        self.face_size = face_size
        self.faces = faces
        self.face_positions = face_positions
        self.orientations = orientations
        self.face_at_position = {position: face_id for face_id, position in face_positions.items()}
        self.face_at_normal = {normal: face_id for face_id, (normal, _, _) in orientations.items()}


    @classmethod
    def from_grid(cls, grid: Grid) -> "Cube":
        """Identify six equal faces and fold their 2D net into a cube."""
        face_size = int((len(grid.values) // 6) ** 0.5)
        face_tiles = defaultdict(dict)
        for row, col in grid:
            position = row // face_size, col // face_size
            face_tiles[position][row % face_size, col % face_size] = grid.at(row, col)
        assert len(face_tiles) == 6

        first = next(iter(face_tiles))
        orientations = {first: ((0, 0, 1), (1, 0, 0), (0, -1, 0))}
        queue = deque([first])
        while queue:
            position = queue.popleft()
            normal, right, down = orientations[position]
            for direction, (dr, dc) in enumerate(cls.DIRS):
                neighbor = position[0] + dr, position[1] + dc
                if neighbor not in face_tiles or neighbor in orientations:
                    continue
                if direction == 0:
                    orientation = (right, _neg(normal), down)
                elif direction == 1:
                    orientation = (down, right, _neg(normal))
                elif direction == 2:
                    orientation = (_neg(right), normal, down)
                else:
                    orientation = (_neg(down), right, normal)
                orientations[neighbor] = orientation
                queue.append(neighbor)
        assert len(orientations) == 6

        face_positions = {face_id: position for face_id, position in enumerate(face_tiles, start=1)}
        faces = {face_id: CubeFace(face_id, face_tiles[position]) for face_id, position in face_positions.items()}
        orientations = {face_id: orientations[position] for face_id, position in face_positions.items()}
        return cls(face_size, faces, face_positions, orientations)

    def map_point(self, row: int, col: int) -> tuple[int, int, int]:
        """
        Given (row, col) coordinates of the original puzzle input, returns the (face_id, local_row, local_col) coordinates
        on the Cube.
        """
        position = row // self.face_size, col // self.face_size
        return self.face_at_position[position], row % self.face_size, col % self.face_size

    def unmap_point(self, face_id: int, row: int, col: int) -> tuple[int, int]:
        """Map face-local coordinates back to the original grid."""
        face_row, face_col = self.face_positions[face_id]
        return face_row * self.face_size + row, face_col * self.face_size + col

    def cross_edge(
        self,
        face_id: int,
        row: int,
        col: int,
        direction: int,
    ) -> tuple[int, int, int, int]:
        """Return ``(face_id, row, col, direction)`` after crossing an edge."""
        normal, right, down = self.orientations[face_id]
        outgoing = (right, down, _neg(right), _neg(down))[direction]
        destination = self.face_at_normal[outgoing]
        _, destination_right, destination_down = self.orientations[destination]
        new_heading = _neg(normal)
        new_direction = (destination_right, destination_down, _neg(destination_right), _neg(destination_down)).index(new_heading)
        offset = row if direction in (0, 2) else col
        source_axis = down if direction in (0, 2) else right
        destination_axis = destination_right if new_direction in (1, 3) else destination_down
        if source_axis == _neg(destination_axis):
            offset = self.face_size - 1 - offset
        else:
            assert source_axis == destination_axis
        last = self.face_size - 1
        if new_direction == 0:
            return destination, offset, 0, new_direction
        if new_direction == 1:
            return destination, 0, offset, new_direction
        if new_direction == 2:
            return destination, offset, last, new_direction
        return destination, last, offset, new_direction
