from typing import List, Tuple, Optional
import random
def parse_config(file_path):
    try:
        requirement = ["WIDTH", "PERFECT"]
        with open(file_path, "r") as f:
            f.read()
            for i in requirement:
                if i not in f:
                    raise ValueError(f"missing parametre {i}")
    except  ValueError as e:
        print(f"Error: {e}")  

def validate_params(entry, exit):
    return entry == MazeGenerator.self.entry and exit == MazeGenerator.self.exit

class MazeGenerator:
    DIRECTIONS = {
    "N": (0, -1, 1), # (dx, dy, current_bit)
    "E": (1, 0, 2),
    "S": (0, 1, 4),
    "W": (-1, 0, 8)
    }
    # this dictionnaire is for shared walls, 1 for the current is the 4 for the next wall cell
    OPPOSITE = {1: 4, 2: 8, 4: 1, 8: 2}

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: List[List[int]] = [[0xF for _ in range(width)] for _ in range(height)]
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (width - 1, height - 1)
    
    def in_bounds(self, x: int, y: int) -> bool:
        return (0 <= x < self.width and 0 <= y < self.height)
        """this methode helps to prevent the out of index eurror"""
    
    def get_neighbors(self, x: int, y: int) -> list[Tuple[int, int, int]]:
        valid_nighbors = []
        for dx, dy, bit in self.DIRECTIONS.values():
            nx, ny = x + dx, y + dy
            
            if self.in_bounds(nx, ny):
                #i should add here the verification if the cell is visited
                valid_nighbors.append(nx, ny, bit)
        return valid_nighbors        

    def generate(self, start_x: int, start_y: int) -> None:
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True
        cx, cy = stack[-1]
        neighbors = self.get_neighbors(cx, cy)
        while stack:
            if neighbors:
                nx, ny, bit = random.choice(neighbors)
                
                #oppenning the walls
                self.grid[cy][cx] &= ~bit
                self.grid[ny][nx] &= ~self.OPPOSITE[bit]


                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()
    def get_shortest_path(self) -> str:
        """Returns the solution as a string of N, E, S, W[cite: 156]."""
        pass

    def save_to_file(self, filename: str, contenant: str) -> None:
        """Writes the hex grid and path to the output file[cite: 145, 155]."""
        try:
            with open(filename, 'r') as f:
                f.write(contenant)

MazeGenerator.generate(0, 0)

