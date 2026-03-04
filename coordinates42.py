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
        """Calculates the list of cells comprising the '42' logo.

        Determines the coordinates for the '4' and '2' digit patterns
        based on the center of the provided maze dimensions.

        Args:
            maze_w (int): The total width of the maze.
            maze_h (int): The total height of the maze.

        Returns:
            List[Tuple[int, int]]: A list of (x, y) coordinates representing
                the logo's structural blocks.
        """
        mid_x = maze_w // 2
        mid_y = maze_h // 2

        cells = [
            (mid_x + 2, mid_y - 2),
            (mid_x + 1, mid_y - 2),
            (mid_x + 3, mid_y - 2),
            (mid_x + 3, mid_y - 1),
            (mid_x + 3, mid_y),
            (mid_x + 2, mid_y),
            (mid_x + 1, mid_y),
            (mid_x + 1, mid_y + 1),
            (mid_x + 1, mid_y + 2),
            (mid_x + 2, mid_y + 2),
            (mid_x + 3, mid_y + 2),
            # Transition to second digit
            (mid_x - 3, mid_y - 2),
            (mid_x - 3, mid_y - 1),
            (mid_x - 3, mid_y),
            (mid_x - 3, mid_y + 1),
            (mid_x - 2, mid_y + 1),
            (mid_x - 1, mid_y),
            (mid_x - 1, mid_y + 1),
            (mid_x - 1, mid_y + 2)
        ]
        return cells