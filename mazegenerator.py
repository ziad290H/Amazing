from typing import List, Tuple, Optional
import random

class MazeGenerator:
    DIRECTIONS = {
        "N": (0, -1, 1), # dx, dy, bit
        "E": (1, 0, 2),
        "S": (0, 1, 4),
        "W": (-1, 0, 8)
    }
    OPPOSITE = {1: 4, 2: 8, 4: 1, 8: 2}

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(str(seed))
        self.grid = [[0xF for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def enforce_borders(self):
        for y in range(self.height):
            for x in range(self.width):
                if y == 0: self.grid[y][x] |= 1
                if x == self.width - 1: self.grid[y][x] |= 2
                if y == self.height - 1: self.grid[y][x] |= 4
                if x == 0: self.grid[y][x] |= 8

    def apply_42_logo(self) -> None:
        # 5x7 pattern where 1 = fully closed cell (Hex F)
        # This represents a clear '4' and '2'
        pattern = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        p_h = len(pattern)
        p_w = len(pattern[0])

        # Validation: Check if maze can fit the logo + 1 cell border [cite: 144]
        if self.width < p_w + 2 or self.height < p_h + 2:
            print("Error: Maze size too small to contain the '42' pattern.") [cite: 145]
            return

        # Calculate centering offsets
        start_x = (self.width - p_w) // 2
        start_y = (self.height - p_h) // 2

        for y in range(p_h):
            for x in range(p_w):
                if pattern[y][x] == 1:
                    target_x, target_y = start_x + x, start_y + y
                    # Set all bits to 1 (Value 15 / Hex F) [cite: 148]
                    self.grid[target_y][target_x] = 15 
                    # Mark as visited so generator ignores these cells
                    self.visited[target_y][target_x] = True

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        valid = []
        for dx, dy, bit in self.DIRECTIONS.values():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and not self.visited[ny][nx]:
                valid.append((nx, ny, bit))
        return valid

    def generate(self, start_x: int, start_y: int) -> None:
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        while stack:
            cx, cy = stack[-1]
            neighbors = self.get_neighbors(cx, cy)

            if neighbors:
                nx, ny, bit = random.choice(neighbors)
                # Remove walls
                self.grid[cy][cx] &= ~bit
                self.grid[ny][nx] &= ~self.OPPOSITE[bit]
               
                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()
            yield (stack)

    #THIS IS THE BFS!!!!
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        queue = [start]
        parent = {start: None}

        while queue:
            curr = queue.pop(0)
            if curr == end:
                break

            cx, cy = curr
            val = self.grid[cy][cx]

            # Directions: N=1, E=2, S=4, W=8
            moves = []
            if not (val & 1): moves.append((cx, cy - 1))
            if not (val & 2): moves.append((cx + 1, cy))
            if not (val & 4): moves.append((cx, cy + 1))
            if not (val & 8): moves.append((cx - 1, cy))

            for next_node in moves:
                if next_node not in parent:
                    parent[next_node] = curr
                    queue.append(next_node)

        # Reconstruct path
        path = []
        step = end
        while step:
            path.append(step)
            step = parent.get(step)
        return path[::-1]