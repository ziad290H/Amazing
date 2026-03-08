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

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True
    ):
        """Initializes the maze grid and applies optional randomization seed.

        Args:
            width (int): Horizontal dimension of the maze.
            height (int): Vertical dimension of the maze.
            seed (Optional[int]): Random seed for reproducibility.
            perfect (bool): If True, one unique path between any two cells.
            if False, extra walls are removed to create loops/multiple routes.
        """
        self.width = width
        self.height = height
        self.perfect = perfect

        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 10**6)
        self.grid = [[0xF for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]

    def in_bounds(self, x: int, y: int) -> bool:
        """Checks if the given coordinates are within the grid boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

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
        if self.seed:
            random.seed(self.seed)
        # with open("test.txt", "w") as f:
        #     f.write(str(self.seed))
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        while stack:
            cx, cy = stack[-1]
            neighbors = self.get_neighbors(cx, cy)

            if neighbors:
                # unpacking
                nx, ny, bit = random.choice(neighbors)
                self.grid[cy][cx] &= ~bit
                self.grid[ny][nx] &= ~self.OPPOSITE[bit]
                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()
            yield stack

        if not self.perfect:
            self.add_loops()

    def solve(self,
              start: Tuple[int, int],
              end: Tuple[int, int]
              ) -> List[Tuple[int, int]]:
        # BFS
        """Finds the shortest path between two points
                 using Breadth-First Search (BFS).

        This method navigates the maze by checking bitwise wall values. It
        ensures the path only moves through carved-out passages and avoids
        visiting the same coordinate twice.

        Args:
            start (Tuple[int, int]): The (x, y) coordinates
             of the starting point.
            end (Tuple[int, int]): The (x, y) coordinates
             of the destination.

        Returns:
            List[Tuple[int, int]]: A list of (x, y) coordinates
            representing the shortest path from start to end.
            Returns an empty list if no path exists.
        """
        queue = [start]
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            start: None
        }

        while queue:
            curr = queue.pop(0)
            if curr == end:
                # Reconstruction logic
                path = []
                temp_curr: Optional[Tuple[int, int]] = curr
                while temp_curr is not None:
                    path.append(temp_curr)
                    temp_curr = parent[temp_curr]
                return path[::-1]

            cx, cy = curr
            val = self.grid[cy][cx]

            # N=1, E=2, S=4, W=8
            directions = [((cx, cy - 1), 1), ((cx + 1, cy), 2),
                          ((cx, cy + 1), 4), ((cx - 1, cy), 8)]

            for (nx, ny), bit in directions:
                if self.in_bounds(nx, ny) and (nx, ny) not in parent:
                    if not (val & bit):
                        parent[(nx, ny)] = curr
                        queue.append((nx, ny))

        return []  # No path found

    def add_loops(self, loop_factor: float = 0.12) -> None:
        """Removes random interior walls to create loops (imperfect maze).

        Args:
            loop_factor (float): Fraction of candidate walls to remove.
                Default 0.12 gives a loopy but still maze-like feel.
        """
        rng = random.Random(self.seed)
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 15:
                    continue
                for dx, dy, bit in self.DIRECTIONS.values():
                    nx, ny = x + dx, y + dy
                    if not self.in_bounds(nx, ny):
                        continue
                    if self.grid[ny][nx] == 15:
                        continue
                    if (self.grid[y][x] & bit) and rng.random() < loop_factor:
                        self.grid[y][x] &= ~bit
                        self.grid[ny][nx] &= ~self.OPPOSITE[bit]
