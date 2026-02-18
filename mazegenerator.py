from typing import List, Tuple, Optional
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
        self.valid_nighbors = []
        if not in_bounds(self.x, self.y):
            return None
        valid_nighbors.append((x, y,))
        

    def generate(self, perfect: bool = True) -> None:
        pass

    def get_shortest_path(self) -> str:
        """Returns the solution as a string of N, E, S, W[cite: 156]."""
        pass

    def save_to_file(self, filename: str) -> None:
        """Writes the hex grid and path to the output file[cite: 145, 155]."""
        pass