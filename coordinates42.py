from typing import List, Tuple, Dict


class Coordinates:
    """
        Represents the maze coordinates including directions,
        directions opposite and 42 block cells coordinate.
        Kept in sync with mazegen/coordinates42.py so Parser validation
        always matches actual logo placement in the generator.
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
    def _42_cells(maze_w: int, maze_h: int) -> List[Tuple]:
        """
        Calculates logo cells using the exact same logic as MazeGenerator.

        :param maze_w:   the maze width
        :type maze_w:    int
        :param maze_h:   the maze height
        :type maze_h:    int
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
