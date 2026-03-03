from typing import List, Tuple


class HexEncoder:
    """
    Represent the maze hexadecimal output
    """

    bit_map = {'N': 1, 'E': 2, 'S': 4, 'W': 8}
    hex_chars = "0123456789ABCDEF"

    def __init__(self,
                 grid: List[List],
                 width: int,
                 height: int,
                 entry: Tuple[int, int],
                 exit: Tuple[int, int],
                 path: str
                 ) -> None:

        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.path = path

    def encode(self) -> str:
        """
        Converts the integer grid into a hexadecimal string.
        Each integer (0-15) maps directly to its Hex equivalent.
        """
        hex_chars = "0123456789ABCDEF"
        hex_grid = []
        
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                # cell is an integer (0-15) from MazeGenerator.grid
                cell_val = self.grid[y][x]
                # Directly map the integer to its hex character
                row_str += hex_chars[cell_val]
            hex_grid.append(row_str)
    
        wall_block = "\n".join(hex_grid)
        
        # Format the path as a coordinate string if it's a list of tuples
        path_str = ""
        if isinstance(self.path, list):
            path_str = " -> ".join([f"({x},{y})" for x, y in self.path])
        else:
            path_str = str(self.path)
    
        output = (
            f"{wall_block}\n\n"
            f"{self.entry[0]},{self.entry[1]}\n"
            f"{self.exit[0]},{self.exit[1]}\n"
            f"{path_str}"
        )
        return output