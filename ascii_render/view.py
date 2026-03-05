import curses
from typing import Any, Set, Tuple


class MazeView:
    """Provides static methods for rendering game components to the terminal.

    This class handles the visual layout of the Heads-Up Display (HUD),
    the ASCII maze grid, and the interactive control legend.
    """

    @staticmethod
    def draw_hud(stdscr: Any, engine: Any) -> None:
        """Renders the top status bar containing score and health.

        Args:
            stdscr: The main curses window object.
            engine (GameEngine): The engine instance containing data.
        """
        try:
            stdscr.addstr(0, 2, " JUNGLE_PROTOCOL_v2.0 ", curses.A_REVERSE)
            hearts = '❤️ ' * engine.health
            hud = f" SCORE: {engine.score:03d} | HEALTH: {hearts}"
            stdscr.addstr(0, 25, hud, curses.A_BOLD)
        except curses.error:
            pass

    @staticmethod
    def draw_maze(
        stdscr: Any,
        engine: Any,
        path_set: Set[Tuple[int, int]],
        player_char: str,
        them: bool = 1
    ) -> None:
        """Renders the maze grid, walls, player, exit, and solution path.

        Args:
            stdscr: The main curses window object.
            engine (GameEngine): The engine containing grid and player data.
            path_set (Set[Tuple[int, int]]): Solution path coordinates.
            player_char (str): Character representing the player.
        """
        offset_y = 2
        h, w = engine.maze.height, engine.maze.width
        if them == 0:
            wall_attr = curses.A_NORMAL
            logo_attr = curses.A_NORMAL
        elif them == 1:
            wall_attr = curses.color_pair(1)
            logo_attr = curses.color_pair(2)
        else:
            wall_attr = curses.color_pair(3)
            logo_attr = curses.color_pair(2)
        for y in range(h):
            for x in range(w):
                val = engine.maze.grid[y][x]
                py, px = (y * 2) + offset_y, x * 4
                try:
                    stdscr.addstr(py, px, "+", wall_attr)
                    if val == 15:
                        stdscr.addstr(py + 1, px + 1, "███",
                                      logo_attr)
                    if val & 1:
                        stdscr.addstr(py, px + 1, "---",
                                      wall_attr)
                    if val & 8:
                        stdscr.addstr(py + 1, px, "|",
                                      wall_attr)

                    curr = (x, y)
                    if curr == tuple(engine.player_pos):
                        stdscr.addstr(py + 1, px + 2, player_char,
                                      curses.A_BOLD)
                    elif curr == engine.exit:
                        if player_char == "🐒":
                            stdscr.addstr(py + 1, px + 2, "🥥", curses.A_BOLD)
                        if player_char == "🐇":
                            stdscr.addstr(py + 1, px + 2, "🌸", curses.A_BOLD)
                    elif curr in path_set:
                        if player_char == "🐒":
                            stdscr.addstr(py + 1, px + 2, "🍌")
                        elif player_char == "🐇":
                            stdscr.addstr(py + 1, px + 2, "🥕")
                except curses.error:
                    pass
            stdscr.addstr(y * 2 + offset_y, w * 4, "+",
                          wall_attr)
            stdscr.addstr(y * 2 + 1 + offset_y, w * 4, "|",
                          wall_attr)

        for x in range(w):
            stdscr.addstr(h * 2 + offset_y, x * 4, "+---",
                          wall_attr)
        stdscr.addstr(h * 2 + offset_y, w * 4, "+",
                      wall_attr)

    @staticmethod
    def draw_controls(stdscr: Any, engine: Any, sh: int, sw: int) -> None:
        """Displays the interactive control legend at the screen bottom.

        Args:
            stdscr: The main curses window object.
            engine (GameEngine): The engine instance.
            sh (int): Total height of the terminal screen.
            sw (int): Total width of the terminal screen.
        """
        inst_row = (engine.maze.height * 2) + 3
        if inst_row >= sh:
            return
        try:
            stdscr.addstr(inst_row, 0, " " * sw, curses.A_REVERSE)
            btns = [
                (" M ", "ON/OFF"), (" → ", "NEXT"),
                (" P ", "PLAY"), (" S ", "SOLVE"), (" Q ", "QUIT"),
                (" R ", "REGENERATE MAZE"), (" C ", "CHANGE COLOR")
            ]
            curr_x = 2
            for key, label in btns:
                stdscr.addstr(inst_row, curr_x, key,
                              curses.A_BOLD | curses.A_REVERSE)
                stdscr.addstr(inst_row, curr_x + len(key),
                              f" {label}   ", curses.A_REVERSE)
                curr_x += len(key) + len(label) + 4
        except curses.error:
            pass
