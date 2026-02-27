from typing import Tuple, List, Any, Optional, Set
from mazegenerator import MazeGenerator
import curses

class AsciiRenderer:
    def __init__(self,
                 maze: "MazeGenerator",
                 Entry: Tuple[int, int],
                 Exit: Tuple[int, int]
                 ) -> None:

        self.maze = maze
        self.Entry = Entry
        self.Exit = Exit

        self.height = maze.height
        self.width = maze.width

        self.display_grid: List[List[str]] = []
        self.show_path: bool = False
        self.current_color: int = 1

        self.V_WALL = "│"
        self.H_WALL = "─"
        self.CORNER = "+"
        self.EMPTY = " "
        self.FULL_BLOCK = "█"

    def _decode_cell(self, value: int) -> dict:
        return {
            "N": bool(value & 1),
            "E": bool(value & 2),
            "S": bool(value & 4),
            "W": bool(value & 8),
        }

    def _cell_to_display(self, y: int, x: int) -> Tuple[int, int]:
        return 2 * y + 1, 2 * x + 1        

    def _init_display_grid(self) -> None:
        rows = 2 * self.height + 1
        cols = 2 * self.width + 1

        self.display_grid = [
            [" " for _ in range(cols)]
            for _ in range(rows)
        ]

    def _draw_cell(self, y: int, x: int) -> None:
        #  Get cell value
        value = self.maze.grid[y][x]

        # Decode walls
        walls = self._decode_cell(value)

        # Convert coordinates
        disp_y, disp_x = self._cell_to_display(y, x)

        # Draw walls if closed

        # North wall
        if walls["N"]:
            self.display_grid[disp_y - 1][disp_x] = self.H_WALL

        # South wall
        if walls["S"]:
            self.display_grid[disp_y + 1][disp_x] = self.H_WALL

        # West wall
        if walls["W"]:
            self.display_grid[disp_y][disp_x - 1] = self.V_WALL

        # East wall
        if walls["E"]:
            self.display_grid[disp_y][disp_x + 1] = self.V_WALL

    
    def _build_grid(self) -> None:
        # Initialize empty grid
        self._init_display_grid()

        # Loop over maze cells
        for y in range(self.height):
            for x in range(self.width):
                self._draw_cell(y, x)    

    def _draw_entry_exit(self) -> None:
        # Entry
        ey, ex = self.Entry
        disp_y, disp_x = self._cell_to_display(ey, ex)
        self.display_grid[disp_y][disp_x] = "E"

        # Exit
        ey, ex = self.Exit
        disp_y, disp_x = self._cell_to_display(ey, ex)
        self.display_grid[disp_y][disp_x] = "X"        

    def _draw_path(self, path: Set[Tuple[int, int]]) -> None:
        for (y, x) in path:
            disp_y, disp_x = self._cell_to_display(y, x)

            # Don't overwrite entry or exit
            if self.display_grid[disp_y][disp_x] in ("E", "X"):
                continue

            self.display_grid[disp_y][disp_x] = "."
        
    def render(self, stdscr, path: Optional[Set[Tuple[int, int]]] = None) -> None:
    # Clear screen
        stdscr.clear()

        #  Build the maze grid
        self._build_grid()

        # Draw entry & exit
        self._draw_entry_exit()

        # Draw path if provided
        if path:
            self._draw_path(path)

        # Print grid using curses
        for y, row in enumerate(self.display_grid):
            for x, char in enumerate(row):
                stdscr.addch(y, x, char)

        # Refresh screen
        stdscr.refresh()

