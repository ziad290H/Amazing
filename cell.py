class Cell:
    """
        Represents a single square in the maze grid.
        hase attributes:
            walls: dictionary of the 4 walls state
            visited = if the cell was visited or not
            blocked if the cell is owned by 42 block
    """
    flag = True

    def __init__(self) -> None:
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.visited = False
        self.blocked = False
