from typing import List, Tuple, Optional, Dict, Generator
import random


class MazeGenerator:
    """Handles randomized maze generation and pathfinding logic.

    Uses a Recursive Backtracker algorithm for generation and a Breadth-First
    Search (BFS) for solving. Supports custom seeds and '42' logo embedding.

    Attributes:
        DIRECTIONS (Dict): Mapping of cardinal directions to (dx, dy, bitmask).
        OPPOSITE (Dict): Mapping of wall bits to their inverse counterparts.
        width (int): Horizontal dimension of the maze.
        height (int): Vertical dimension of the maze.
        grid (List[List[int]]): 2D array storing bitmask wall data.
        visited (List[List[bool]]): Tracking for generation and logo blocks.
    """

    DIRECTIONS: Dict[str, Tuple[int, int, int]] = {
        "N": (0, -1, 1),
        "E": (1, 0, 2),
        "S": (0, 1, 4),
        "W": (-1, 0, 8)
    }
    OPPOSITE: Dict[int, int] = {1: 4, 2: 8, 4: 1, 8: 2}

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        """Initializes the maze grid and applies optional randomization seed."""
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(str(seed))
        self.grid = [[0xF for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]

    def in_bounds(self, x: int, y: int) -> bool:
        """Checks if the given coordinates are within the grid boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def enforce_borders(self) -> None:
        """Sets bitmask walls for the outer perimeter of the maze."""
        for y in range(self.height):
            for x in range(self.width):
                if y == 0:
                    self.grid[y][x] |= 1
                if x == self.width - 1:
                    self.grid[y][x] |= 2
                if y == self.height - 1:
                    self.grid[y][x] |= 4
                if x == 0:
                    self.grid[y][x] |= 8

    def apply_42_logo(self) -> None:
        """Embeds a static '42' pattern into the center of the maze.

        Cells belonging to the pattern are blocked and marked as visited
        to prevent the generator from carving through them.
        """
        pattern = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        p_h, p_w = len(pattern), len(pattern[0])

        if self.width < p_w + 2 or self.height < p_h + 2:
            print("Error: Maze size too small to contain the '42' pattern.")
            return

        start_x = (self.width - p_w) // 2
        start_y = (self.height - p_h) // 2

        for y in range(p_h):
            for x in range(p_w):
                if pattern[y][x] == 1:
                    target_x, target_y = start_x + x, start_y + y
                    self.grid[target_y][target_x] = 15
                    self.visited[target_y][target_x] = True

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        """Retrieves unvisited adjacent cells for the generation algorithm."""
        valid = []
        for dx, dy, bit in self.DIRECTIONS.values():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and not self.visited[ny][nx]:
                valid.append((nx, ny, bit))
        return valid

    def generate(
        self,
        start_x: int,
        start_y: int
    ) -> Generator[List[Tuple[int, int]], None, None]:
        """Carves paths using a Recursive Backtracker (DFS).

        Yields:
            List[Tuple[int, int]]: The current stack for animation purposes.
        """
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        while stack:
            cx, cy = stack[-1]
            neighbors = self.get_neighbors(cx, cy)

            if neighbors:
                nx, ny, bit = random.choice(neighbors)
                self.grid[cy][cx] &= ~bit
                self.grid[ny][nx] &= ~self.OPPOSITE[bit]
                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()
            yield stack

    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        # Standard BFS__ Breadth-First Search (BFS)
        """Finds the shortest path between two points using Breadth-First Search (BFS).

        This method navigates the maze by checking bitwise wall values. It 
        ensures the path only moves through carved-out passages and avoids 
        visiting the same coordinate twice.

        Args:
            start (Tuple[int, int]): The (x, y) coordinates of the starting point.
            end (Tuple[int, int]): The (x, y) coordinates of the destination.

        Returns:
            List[Tuple[int, int]]: A list of (x, y) coordinates representing the 
                shortest path from start to end. Returns an empty list if 
                no path exists.
        """
        queue = [start]
        parent = {start: None}
    
        while queue:
            curr = queue.pop(0)
            if curr == end:
                # Reconstruction logic
                path = []
                while curr is not None:
                    path.append(curr)
                    curr = parent[curr]
                return path[::-1]

            cx, cy = curr
            val = self.grid[cy][cx]

            # N=1, E=2, S=4, W=8
            # We only move if the BIT is NOT set (meaning the wall is carved out)
            directions = [((cx, cy - 1), 1), ((cx + 1, cy), 2), 
                          ((cx, cy + 1), 4), ((cx - 1, cy), 8)]
    
            for (nx, ny), bit in directions:
                if self.in_bounds(nx, ny) and (nx, ny) not in parent:
                    if not (val & bit): # If there is NO wall in this direction
                        parent[(nx, ny)] = curr
                        queue.append((nx, ny))
        
        return [] # No path found