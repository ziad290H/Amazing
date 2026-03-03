import curses
import time
import os
from typing import Tuple, Optional, List
import pygame


class AsciiRenderer:
    def __init__(
                self,
                maze,
                entry: Tuple[int, int],
                exit_pos: Tuple[int, int],
                player_char="🐒",
                config=None
                 ):
        self.maze = maze
        self.entry = entry
        self.exit = exit_pos
        self.player_char = player_char
        self.config = config

        # Game State
        self.player_pos = list(entry)
        self.score = 0
        self.health = 3
        self.play_mode = False

        # --- MUSIC ENGINE STATE ---
        self.music_playing = False
        self.music_index = 0
        # Change these strings to your actual filenames later
        self.playlist = [
            "saha.mp3",
            "Dance_it_out.mp3",
            "joy_to_the_world.mp3",
            "song3.mp3",
            "song4.mp3"
        ]

    def render(
               self,
               stdscr: curses.window,
               path: Optional[List[Tuple[int, int]]] = None
              ) -> None:
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()
        h, w = self.maze.height, self.maze.width
        path_set = set(path) if path else set()

        # 1. HEADER HUD
        try:
            stdscr.addstr(0, 2, " JUNGLE_PROTOCOL_v2.0 ", curses.A_REVERSE)
            hud = f" SCORE: {self.score:03d} | HEALTH: {'❤️ ' * self.health}"
            stdscr.addstr(0, 25, hud, curses.A_BOLD)
        except curses.error:
            pass

        # 2. MAZE RENDER
        offset_y = 2
        for y in range(h):
            for x in range(w):
                val = self.maze.grid[y][x]
                py, px = (y * 2) + offset_y, x * 4
                try:
                    stdscr.addstr(py, px, "+")
                    if val == 15:
                        stdscr.addstr(py + 1,
                                      px + 1, "███",
                                      curses.color_pair(2))
                    if val & 1:
                        stdscr.addstr(py, px + 1, "---")
                    if val & 8:
                        stdscr.addstr(py + 1, px, "|")

                    curr_cell = (x, y)
                    if curr_cell == tuple(self.player_pos):
                        stdscr.addstr(py + 1,
                                      px + 2,
                                      self.player_char,
                                      curses.A_BOLD)
                    elif curr_cell == self.exit:
                        icon = "🥥" if self.player_char == "🐒" else "🌸"
                        stdscr.addstr(py + 1, px + 2, icon, curses.A_BOLD)
                    elif curr_cell in path_set:
                        icon = "🍌" if self.player_char == "🐒" else "🥕"
                        stdscr.addstr(py + 1, px + 2, icon)
                except curses.error:
                    pass
            try:
                stdscr.addstr(y * 2 + offset_y, w * 4, "+")
                stdscr.addstr(y * 2 + 1 + offset_y, w * 4, "|")
            except curses.error:
                pass

        for x in range(w):
            try:
                stdscr.addstr(h * 2 + offset_y, x * 4, "+---")
            except curses.error:
                pass
        try:
            stdscr.addstr(h * 2 + offset_y, w * 4, "+")
        except curses.error:
            pass

        # 3. STYLED COMMAND BAR
        inst_row = (h * 2) + offset_y + 1
        if inst_row < sh:
            try:
                # Background Highlight Bar
                stdscr.addstr(inst_row, 0, " " * sw, curses.A_REVERSE)

                # Visual buttons for the UI
                controls = [
                    (" M ", "ON/OFF"),
                    (" → ", "NEXT SONG"),
                    (" P ", "PLAY"),
                    (" S ", "SOLVE"),
                    (" Q ", "QUIT")
                ]

                curr_x = 2
                for key, label in controls:
                    stdscr.addstr(inst_row,
                                  curr_x,
                                  key,
                                  curses.A_BOLD | curses.A_REVERSE)
                    stdscr.addstr(inst_row,
                                  curr_x + len(key),
                                  f" {label}  ",
                                  curses.A_REVERSE)
                    curr_x += len(key) + len(label) + 4

                # 4. SYSTEM STATUS (Music Info)
                status_y = inst_row + 2
                if status_y < sh:
                    current_track = self.playlist[self.music_index]
                    if self.music_playing:
                        music_icon = "🔊 ACTIVE"
                    else:
                        music_icon = "🔇 MUTED"
                    music_attr = (curses.color_pair(1)
                                  if self.music_playing else curses.A_DIM)

                    stdscr.addstr(status_y, 2, "SYSTEM » ", curses.A_BOLD)
                    stdscr.addstr(status_y,
                                  11,
                                  f"MUSIC: {music_icon}",
                                  music_attr
                                  )
                    stdscr.addstr(status_y, 28, "NOW PLAYING:", curses.A_DIM)

                    # Highlight the file path of the current song
                    track_display = f" music/{current_track} "
                    stdscr.addstr(status_y, 41, track_display, curses.A_REVERSE if self.music_playing else curses.A_NORMAL)
            except curses.error:
                pass

        stdscr.refresh()

    def switch_music(self):
        """Changes track to the next one in the playlist folder."""
        try:
            self.music_index = (self.music_index + 1) % len(self.playlist)
            track_path = os.path.join("music", self.playlist[self.music_index])

            pygame.mixer.music.load(track_path)
            # If player had music on, start playing the new song immediately
            if self.music_playing:
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def handle_move(self, direction, stdscr):
        x, y = self.player_pos
        val = self.maze.grid[y][x]
        move_map = {
            curses.KEY_UP: (0, -1, 1),
            curses.KEY_RIGHT: (1, 0, 2),
            curses.KEY_DOWN: (0, 1, 4),
            curses.KEY_LEFT: (-1, 0, 8)
        }
        if direction not in move_map:
            return
        dx, dy, wall_bit = move_map[direction]
        nx, ny = x + dx, y + dy

        has_wall = (val & wall_bit) != 0
        is_blocked = (0 <= nx < self.maze.width and 0 <= ny < self.maze.height and self.maze.grid[ny][nx] == 15)

        if not has_wall and not is_blocked:
            self.player_pos[0], self.player_pos[1] = nx, ny
            if tuple(self.player_pos) == self.exit:
                self.score += 10
                if self.health < 3: self.health += 1
                self.regenerate_game()
        else:
            self.health -= 1
            if self.health <= 0:
                self.show_game_over(stdscr)
                self.regenerate_game()

    def show_game_over(self, stdscr: curses.window) -> None:
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except BaseException:
            pass
        sh, sw = stdscr.getmaxyx()
        stdscr.bkgd(' ', curses.color_pair(2) | curses.A_REVERSE)
        stdscr.clear()
        msg = "!!! GAME OVER !!!"
        stdscr.addstr(sh//2, (sw-len(msg))//2, msg, curses.A_BOLD)
        stdscr.refresh()
        time.sleep(3)
        self.score, self.health, self.play_mode = 0, 3, False
        stdscr.bkgd(' ', curses.color_pair(0))

    def regenerate_game(self):
        self.maze.grid = [[0xF for _ in range(self.maze.width)] for _ in range(self.maze.height)]
        self.maze.visited = [[False for _ in range(self.maze.width)] for _ in range(self.maze.height)]
        if hasattr(self.maze, 'apply_42_logo'): self.maze.apply_42_logo()
        self.maze.generate(self.entry[0], self.entry[1])
        self.player_pos = list(self.entry)

    def animate_path(self, stdscr, path):
        if not path:
            return
        for i in range(1, len(path) + 1):
            self.render(stdscr, path[:i])
            curses.napms(50)

    def run(self, stdscr: curses.window) -> None:
        # Initialize Audio Engine
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            track_path = os.path.join("music", self.playlist[self.music_index])
            pygame.mixer.music.load(track_path)
        except:
            pass

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_YELLOW, -1)
        curses.init_pair(2, curses.COLOR_MAGENTA, -1)
        stdscr.keypad(True)
        show_solution = False

        while True:
            path = self.maze.solve(tuple(self.player_pos), self.exit)
            self.render(stdscr, path if show_solution else None)
            key = stdscr.getch()

            if key in (ord('q'), ord('Q'), 27): break

            # [M] - Toggle Music
            if key in (ord('m'), ord('M')):
                try:
                    if self.music_playing:
                        pygame.mixer.music.pause()
                        self.music_playing = False
                    else:
                        pygame.mixer.music.play(-1)
                        self.music_playing = True
                except:
                    pass

            # [Right Arrow] - Next Track
            elif key == curses.KEY_RIGHT:
                self.switch_music()

            # Gameplay Logic
            if self.play_mode:
                if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
                    self.handle_move(key, stdscr)
                elif key in (ord('p'), ord('P')): self.play_mode = False
            else:
                if key in (ord('p'), ord('P')):
                    self.play_mode = True
                    self.player_pos = list(self.entry)
                elif key in (ord('s'), ord('S')):
                    show_solution = not show_solution
                    if show_solution:
                        self.animate_path(stdscr, path)
                elif key in (ord('r'), ord('R')):
                    self.regenerate_game()
