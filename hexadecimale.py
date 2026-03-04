from typing import List, Tuple, Dict


class HexEncoder:
    """Represents the maze hexadecimal output and path encoding.

    This class handles the conversion of a numeric maze grid into a
    hexadecimal string representation and translates a coordinate-based
    path into cardinal direction instructions (N, E, S, W).

    Attributes:
        bit_map (Dict[str, int]): Mapping of directions to their bit values.
        hex_chars (str): Valid characters for hexadecimal representation.
    """

    bit_map: Dict[str, int] = {'N': 1, 'E': 2, 'S': 4, 'W': 8}
    hex_chars: str = "0123456789ABCDEF"

    def __init__(
        self,
        grid: List[List[int]],
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        path: List[Tuple[int, int]]
    ) -> None:
        """Initializes the HexEncoder with maze data and solution path.

        Args:
            grid (List[List[int]]): The 2D grid containing wall bitmasks.
            height (int): The vertical dimension of the maze.
            entry (Tuple[int, int]): Starting (x, y) coordinates.
            exit (Tuple[int, int]): Ending (x, y) coordinates.
            path (List[Tuple[int, int]]): Ordered list of solution coordinates.
        """
        self.grid: List[List[int]] = grid
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.path: List[Tuple[int, int]] = path

    def encode(self) -> str:
        """Assembles the maze data into a formatted SWS output string.

        Returns:
            str: A multi-line string containing the hex grid, entry/exit
                coordinates, and the directional path string.
        """
        # 1. Hex Grid
        hex_rows = ["".join(f"{cell:X}" for cell in row) for row in self.grid]
        wall_block = "\n".join(hex_rows)

        # 2. Convert Coordinate Path to Directional String (N, E, S, W)
        directions: List[str] = []
        for i in range(len(self.path) - 1):
            curr = self.path[i]
            nxt = self.path[i + 1]

            dx = nxt[0] - curr[0]
            dy = nxt[1] - curr[1]

            if dy == -1:
                directions.append("N")
            elif dy == 1:
                directions.append("S")
            elif dx == 1:
                directions.append("E")
            elif dx == -1:
                directions.append("W")

        path_str = "".join(directions)

        # 3. Assemble SWS format
        return (
            f"{wall_block}\n\n"
            f"{self.entry[0]},{self.entry[1]}\n"
            f"{self.exit[0]},{self.exit[1]}\n"
            f"{path_str}"
        )