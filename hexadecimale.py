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
        # 1. Hex Grid
        hex_rows = ["".join(f"{cell:X}" for cell in row) for row in self.grid]
        wall_block = "\n".join(hex_rows)
        
        # 2. Convert Coordinate Path to Directional String (N, E, S, W)
        directions = []
        for i in range(len(self.path) - 1):
            curr = self.path[i]
            nxt = self.path[i+1]
            
            dx = nxt[0] - curr[0]
            dy = nxt[1] - curr[1]
            
            if dy == -1: directions.append("N")
            elif dy == 1: directions.append("S")
            elif dx == 1: directions.append("E")
            elif dx == -1: directions.append("W")
        
        path_str = "".join(directions)
    
        # 3. Assemble SWS format
        return (
            f"{wall_block}\n\n"
            f"{self.entry[0]},{self.entry[1]}\n"
            f"{self.exit[0]},{self.exit[1]}\n"
            f"{path_str}"
        )