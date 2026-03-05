import curses


class MazeView:
    @staticmethod
    def draw_hud(stdscr, engine):
        try:
            stdscr.addstr(0, 2, " JUNGLE_PROTOCOL_v2.0 ", curses.A_REVERSE)
            hearts = '❤️ ' * engine.health
            hud = f" SCORE: {engine.score:03d} | HEALTH: {hearts}"
            stdscr.addstr(0, 25, hud, curses.A_BOLD)
        except curses.error:
            pass

    @staticmethod
    def draw_maze(stdscr, engine, path_set, player_char):
        offset_y = 2
        h, w = engine.maze.height, engine.maze.width
        for y in range(h):
            for x in range(w):
                val = engine.maze.grid[y][x]
                py, px = (y * 2) + offset_y, x * 4
                try:
                    stdscr.addstr(py, px, "+")
                    if val == 15:
                        stdscr.addstr(py + 1, px + 1, "███",
                                      curses.color_pair(2))
                    if val & 1:
                        stdscr.addstr(py, px + 1, "---")
                    if val & 8:
                        stdscr.addstr(py + 1, px, "|")

                    curr = (x, y)
                    if curr == tuple(engine.player_pos):
                        stdscr.addstr(py + 1, px + 2, player_char,
                                      curses.A_BOLD)
                    elif curr == engine.exit:
                        stdscr.addstr(py + 1, px + 2, "🥥", curses.A_BOLD)
                    elif curr in path_set:
                        stdscr.addstr(py + 1, px + 2, "🍌")
                except curses.error:
                    pass
            stdscr.addstr(y * 2 + offset_y, w * 4, "+")
            stdscr.addstr(y * 2 + 1 + offset_y, w * 4, "|")

        for x in range(w):
            stdscr.addstr(h * 2 + offset_y, x * 4, "+---")
        stdscr.addstr(h * 2 + offset_y, w * 4, "+")

    @staticmethod
    def draw_controls(stdscr, engine, sh, sw):
        inst_row = (engine.maze.height * 2) + 3
        if inst_row >= sh:
            return
        try:
            stdscr.addstr(inst_row, 0, " " * sw, curses.A_REVERSE)
            btns = [
                (" M ", "ON/OFF"), (" → ", "NEXT"),
                (" P ", "PLAY"), (" S ", "SOLVE"), (" Q ", "QUIT")
            ]
            curr_x = 2
            for key, label in btns:
                stdscr.addstr(inst_row, curr_x, key,
                              curses.A_BOLD | curses.A_REVERSE)
                stdscr.addstr(inst_row, curr_x + len(key),
                              f" {label}  ", curses.A_REVERSE)
                curr_x += len(key) + len(label) + 4
        except curses.error:
            pass