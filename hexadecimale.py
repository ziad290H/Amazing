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
        Docstring for encode
        the encoder method
        :return: it return the maze hexadicimal output
        :rtype: str
        """
        hex_grid = []
        for y in range(0, self.height):
            row_str = ""
            for x in range(0, self.width):
                cell_sum = 0
                cell = self.grid[y][x]
                for direction, bit_value in self.bit_map.items():
                    if cell.walls[direction] is True:
                        cell_sum += bit_value
                row_str += self.hex_chars[cell_sum]
            hex_grid.append(row_str)

        wall_block = "\n".join(hex_grid)
        output = (
            f"{wall_block}\n\n"
            f"{self.entry[0]},{self.entry[1]}\n"
            f"{self.exit[0]},{self.exit[1]}\n"
            f"{self.path}"
        )
        return output