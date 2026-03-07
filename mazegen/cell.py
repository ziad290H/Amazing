from typing import Dict


class Cell:
    """Represents a single square in the maze grid.

    This class tracks the state of the four surrounding walls, whether
    the cell has been processed by the generation algorithm, and if it
    is part of a static structural block.

    Attributes:
        walls (Dict[str, bool]): A mapping of directions ('N', 'E', 'S', 'W')
            to their respective wall states
            (True for exists, False for carved).
        visited (bool): True if the cell has been visited during generation.
        blocked (bool): True if the cell is part of the '42' logo block.
    """


    def __init__(self) -> None:
        """Initializes a new maze cell with all walls intact and unvisited."""
        self.walls: Dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited: bool = False
        self.blocked: bool = False
