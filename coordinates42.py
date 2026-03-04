from typing import List, Tuple


class Coordinates:
    """
        Represents the maze coordinates including directions,
        directions oposite and 42 bleck cells coordinate
    """
    directions = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'W': (-1, 0),
    }
    opposite = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E',
    }

    @staticmethod
    def _42_cells(
            maze_w: int,
            maze_h: int
                            ) -> List[Tuple]:
        """
        Docstring for _42_cells

        :param maze_width:		the maze width
        :type maze_width:		int
        :param maze_height:		the maze height
        :type maze_height:		int
        """
        cells = [
            ((maze_w // 2) + 2, (maze_h // 2) - 2),
            ((maze_w // 2) + 1, (maze_h // 2) - 2),
            ((maze_w // 2) + 3, (maze_h // 2) - 2),
            ((maze_w // 2) + 3, (maze_h // 2) - 1),
            ((maze_w // 2) + 3, (maze_h // 2)),
            ((maze_w // 2) + 2, (maze_h // 2)),
            ((maze_w // 2) + 1, (maze_h // 2)),
            ((maze_w // 2) + 1, (maze_h // 2) + 1),
            ((maze_w // 2) + 1, (maze_h // 2) + 2),
            ((maze_w // 2) + 2, (maze_h // 2) + 2),
            ((maze_w // 2) + 3, (maze_h // 2) + 2),
            \
            ((maze_w // 2) - 3, (maze_h // 2) - 2),
            ((maze_w // 2) - 3, (maze_h // 2) - 1),
            ((maze_w // 2) - 3, (maze_h // 2)),
            ((maze_w // 2) - 3, (maze_h // 2) + 1),
            ((maze_w // 2) - 2, (maze_h // 2) + 1),
            ((maze_w // 2) - 1, (maze_h // 2)),
            ((maze_w // 2) - 1, (maze_h // 2) + 1),
            ((maze_w // 2) - 1, (maze_h // 2) + 2)
        ]
        return cells
