import curses
import time
import os
import random
from typing import Tuple, Optional, List
import pygame


class AsciiRenderer:
    def __init__(self, maze, entry: Tuple[int, int], exit_pos: Tuple[int, int], player_char="🐒", config=None):
        self.maze = maze
        self.entry = entry
        self.exit = exit_pos
        self.player_char = player_char
        self.config = config
        self.player_pos = list(entry)
        self.score = 0
        self.health = 3
        self.play_mode = False
        self.music_playing = False
        self.music_index = 0
        self.playlist = [
            "saha.mp3",
            "Dance_it_out.mp3",
            "joy_to_the_world.mp3",
            "song3.mp3",
            "song4.mp3"
        ]

    def render(self, stdscr: curses.window, path: Optional[List[Tuple[int, int]]] = None) -> None:
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()
        h, w = self.maze.height, self.maze.width
        path_set = set(path) if path else set()
        try:
            stdscr.addstr(0, 2, " JUNGLE_PROTOCOL_v2.0 ", curses.A_REVERSE)
            hud = f" SCORE: {self.score:03d} | HEALTH: {'❤️ ' * self.health}"
            stdscr.addstr(0, 25, hud, curses.A_BOLD)
        except curses.error:
            pass
        offset_y = 2
        for y in range(h):
            for x in range(w):
                val = self.maze.grid[y][x]
                py, px = (y * 2) + offset_y, x * 4
                try:
                    stdscr.addstr(py, px, "+")
                    if val == 15:
                        stdscr.addstr(py + 1, px + 1, "███", curses.color_pair(2))
                    if val & 1:
                        stdscr.addstr(py, px + 1, "---")
                    if val & 8:
                        stdscr.addstr(py + 1, px, "|")
                    curr_cell = (x, y)
                    if curr_cell == tuple(self.player_pos):
                        stdscr.addstr(py + 1, px + 2, self.player_char, curses.A_BOLD)
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
        inst_row = (h * 2) + offset_y + 1
        if inst_row < sh:
            try:
                stdscr.addstr(inst_row, 0, " " * sw, curses.A_REVERSE)
                controls = [
                    (" M ", "ON/OFF"),
                    (" N ", "NEXT SONG"),
                    (" P ", "PLAY"),
                    (" S ", "SOLVE"),
                    (" Q ", "QUIT")
                ]
                curr_x = 2
                for key, label in controls:
                    stdscr.addstr(inst_row, curr_x, key, curses.A_BOLD | curses.A_REVERSE)
                    stdscr.addstr(inst_row, curr_x + len(key), f" {label}  ", curses.A_REVERSE)
                    curr_x += len(key) + len(label) + 4
                status_y = inst_row + 2
                if status_y < sh:
                    current_track = self.playlist[self.music_index]
                    music_icon = "🔊 ACTIVE" if self.music_playing else "🔇 MUTED"
                    music_attr = curses.color_pair(1) if self.music_playing else curses.A_DIM
                    stdscr.addstr(status_y, 2, "SYSTEM » ", curses.A_BOLD)
                    stdscr.addstr(status_y, 11, f"MUSIC: {music_icon}", music_attr)
                    stdscr.addstr(status_y, 28, "NOW PLAYING:", curses.A_DIM)
                    track_display = f" music/{current_track} "
                    stdscr.addstr(status_y, 41, track_display,
                                  curses.A_REVERSE if self.music_playing else curses.A_NORMAL)
            except curses.error:
                pass
        stdscr.refresh()

    def switch_music(self):
        try:
            self.music_index = (self.music_index + 1) % len(self.playlist)
            track_path = os.path.join("music", self.playlist[self.music_index])
            pygame.mixer.music.load(track_path)
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
        is_blocked = (0 <= nx < self.maze.width and 0 <= ny < self.maze.height
                      and self.maze.grid[ny][nx] == 15)
        if not has_wall and not is_blocked:
            self.player_pos[0], self.player_pos[1] = nx, ny
            if tuple(self.player_pos) == self.exit:
                self.score += 10
                if self.health < 3:
                    self.health += 1
                self.regenerate_game(stdscr)
        else:
            self.health -= 1
            if self.health <= 0:
                self.show_game_over(stdscr)
                self.regenerate_game(stdscr)

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
        stdscr.addstr(sh // 2, (sw - len(msg)) // 2, msg, curses.A_BOLD)
        stdscr.refresh()
        time.sleep(3)
        self.score, self.health, self.play_mode = 0, 3, False
        stdscr.bkgd(' ', curses.color_pair(0))

    def regenerate_game(self, stdscr: Optional[curses.window] = None):
        self.maze.grid = [[0xF for _ in range(self.maze.width)] for _ in range(self.maze.height)]
        self.maze.visited = [[False for _ in range(self.maze.width)] for _ in range(self.maze.height)]
        if hasattr(self.maze, 'apply_42_logo'):
            self.maze.apply_42_logo()
        if stdscr:
            stack = [self.entry]
            self.maze.visited[self.entry[1]][self.entry[0]] = True
            dirs = [(0, -1, 1, 4), (1, 0, 2, 8), (0, 1, 4, 1), (-1, 0, 8, 2)]
            while stack:
                x, y = stack[-1]
                neighbors = []
                for dx, dy, w1, w2 in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                        if not self.maze.visited[ny][nx] and self.maze.grid[ny][nx] == 0xF:
                            neighbors.append((nx, ny, w1, w2))
                if neighbors:
                    nx, ny, w1, w2 = random.choice(neighbors)
                    self.maze.grid[y][x] &= ~w1
                    self.maze.grid[ny][nx] &= ~w2
                    self.maze.visited[ny][nx] = True
                    stack.append((nx, ny))
                    self.render(stdscr)
                    curses.napms(10)
                else:
                    stack.pop()
                    self.render(stdscr)
                    curses.napms(5)
        else:
            self.maze.generate(self.entry[0], self.entry[1])
        self.player_pos = list(self.entry)

    def animate_path(self, stdscr, path):
        if not path:
            return
        for i in range(1, len(path) + 1):
            self.render(stdscr, path[:i])
            curses.napms(50)

    def run(self, stdscr: curses.window) -> None:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            track_path = os.path.join("music", self.playlist[self.music_index])
            pygame.mixer.music.load(track_path)
        except Exception:
            pass
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_YELLOW, -1)
        curses.init_pair(2, curses.COLOR_MAGENTA, -1)
        stdscr.keypad(True)
        show_solution = False
        self.regenerate_game(stdscr)

        while True:
            path = self.maze.solve(tuple(self.player_pos), self.exit)
            self.render(stdscr, path if show_solution else None)
            key = stdscr.getch()
            if key in (ord('q'), ord('Q'), 27):
                break
            if key in (ord('m'), ord('M')):
                try:
                    if self.music_playing:
                        pygame.mixer.music.pause()
                        self.music_playing = False
                    else:
                        pygame.mixer.music.play(-1)
                        self.music_playing = True
                except Exception:
                    pass
            elif key in (ord('n'), ord('N')):
                self.switch_music()
            if self.play_mode:
                if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
                    self.handle_move(key, stdscr)
                elif key in (ord('p'), ord('P')):
                    self.play_mode = False
            else:
                if key in (ord('p'), ord('P')):
                    self.play_mode = True
                    self.player_pos = list(self.entry)
                elif key in (ord('s'), ord('S')):
                    show_solution = not show_solution
                    if show_solution:
                        self.animate_path(stdscr, path)
                elif key in (ord('r'), ord('R')):
                    self.regenerate_game(stdscr)
