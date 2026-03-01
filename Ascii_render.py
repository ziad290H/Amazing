import curses
from typing import Tuple, Optional, Set, List

class AsciiRenderer:
    def __init__(self, maze, entry: Tuple[int, int], exit_pos: Tuple[int, int]):
        self.maze = maze
        self.entry = entry
        self.exit = exit_pos

    def render(self, stdscr, path: Optional[List[Tuple[int, int]]] = None):
        """
        Renders the maze grid, walls, entry/exit points, and the solution path.
        """
        stdscr.clear()
        h, w = self.maze.height, self.maze.width
        path_set = set(path) if path else set()
        
        for y in range(h):
            for x in range(w):
                val = self.maze.grid[y][x]
                py, px = y * 2, x * 4
                
                # Draw the corner node
                stdscr.addstr(py, px, "+")
                
                if val == 15:
                    # Use a specific color pair for the 42 pattern cells
                    stdscr.addstr(py + 1, px + 1, "███", curses.color_pair(2))

                # North Wall logic (Bit 1)
                if val & 1:
                    stdscr.addstr(py, px + 1, "---")
                else:
                    stdscr.addstr(py, px + 1, "   ")
                    
                # West Wall logic (Bit 8)
                if val & 8:
                    stdscr.addstr(py + 1, px, "|")
                else:
                    stdscr.addstr(py + 1, px, " ")

                # Cell Content Logic
                if (x, y) == self.entry:
                    stdscr.addstr(py + 1, px + 2, "🐒", curses.A_BOLD)
                elif (x, y) == self.exit:
                    stdscr.addstr(py + 1, px + 2, "🥥", curses.A_BOLD)
                elif (x, y) in path_set:
                    try:
                        stdscr.addstr(py + 1, px + 2, "🍌")
                    except curses.error:
                        stdscr.addstr(py + 1, px + 2, "o", curses.color_pair(1))

            # Draw East boundary for the current row
            stdscr.addstr(y * 2, w * 4, "+")
            stdscr.addstr(y * 2 + 1, w * 4, "|")

        # Draw the final South boundary of the maze
        for x in range(w):
            stdscr.addstr(h * 2, x * 4, "+---")
        stdscr.addstr(h * 2, w * 4, "+")

        # --- Instructions Block ---
        instruction_row = (h * 2) + 2
        instructions = [
            "CONTROLS:",
            "  [R] - Regenerate Maze",
            "  [S] - Toggle Shortest Path",
            "  [Q] - Quit Application"
        ]
        for i, text in enumerate(instructions):
            try:
                stdscr.addstr(instruction_row + i, 2, text, curses.A_DIM)
            except curses.error:
                pass
        
        stdscr.refresh()

    def run(self, stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        
        show_solution = False
        
        while True:
            # Re-calculate path every loop to handle regeneration
            path = self.maze.solve(self.entry, self.exit)
            self.render(stdscr, path if show_solution else None)
            
            key = stdscr.getch()
            
            if key in (ord('q'), ord('Q'), 27): # Quit
                break
            if key in (ord('s'), ord('S')):     # Toggle Solution
                show_solution = not show_solution
            if key in (ord('r'), ord('R')):     # Regenerate
                # Clear existing state
                self.maze.grid = [[0xF for _ in range(self.maze.width)] for _ in range(self.maze.height)]
                self.maze.visited = [[False for _ in range(self.maze.width)] for _ in range(self.maze.height)]
                # Re-apply logo and generate
                if hasattr(self.maze, 'apply_42_logo'):
                    self.maze.apply_42_logo()
                self.maze.generate(self.entry[0], self.entry[1])