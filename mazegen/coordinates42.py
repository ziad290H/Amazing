from typing import List, Tuple, Dict


class Coordinates:
    """Represents maze coordinates and structural metadata.

    This class provides static mappings for cardinal directions, their
    opposites, and calculates the specific coordinate offsets used to
    render the '42' logo within the maze grid.

    Attributes:
        directions (Dict[str, Tuple[int, int]]): Mapping of 'N', 'S', 'E', 'W'
            to coordinate deltas (dx, dy).
        opposite (Dict[str, str]): Mapping of directions to their
            inverse (e.g., 'N' to 'S').
    """

    directions: Dict[str, Tuple[int, int]] = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'W': (-1, 0),
    }
    opposite: Dict[str, str] = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E',
    }

    @staticmethod
    def _42_cells(maze_w: int, maze_h: int) -> List[Tuple[int, int]]:
        """
        Calculates logo cells using the exact same logic as the Generator.
        """
        pattern = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
        p_h, p_w = len(pattern), len(pattern[0])
        start_x = (maze_w - p_w) // 2
        start_y = (maze_h - p_h) // 2
        cells = []
        for y in range(p_h):
            for x in range(p_w):
                if pattern[y][x] == 1:
                    cells.append((start_x + x, start_y + y))
        return cells
