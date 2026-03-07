from typing import Dict


class Cell:
    """A single maze cell tracking its four walls and state."""

    def __init__(self) -> None:
        """Initializes the cell with all walls up and unvisited."""
        self.walls: Dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited: bool = False
        self.blocked: bool = False
