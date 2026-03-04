import curses
import pygame
import os
from .engine import GameEngine
from .view import MazeView


class AsciiRenderer:
    def __init__(self, maze, entry, exit_pos, char="🐒", config=None):
        playlist = [
            "saha.mp3", "Dance_it_out.mp3", "joy_to_the_world.mp3",
            "song3.mp3", "song4.mp3"
        ]
        self.engine = GameEngine(maze, entry, exit_pos, playlist)
        self.player_char = char
        self.config = config

    def render(self, stdscr, path=None):
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()
        path_set = set(path) if path else set()

        MazeView.draw_hud(stdscr, self.engine)
        MazeView.draw_maze(stdscr, self.engine, path_set, self.player_char)
        MazeView.draw_controls(stdscr, self.engine, sh, sw)

        status_y = (self.engine.maze.height * 2) + 5
        if status_y < sh:
            track = self.engine.playlist[self.engine.music_index]
            status = "🔊 ACTIVE" if self.engine.music_playing else "🔇 MUTED"
            msg = f"SYSTEM » MUSIC: {status} | NOW PLAYING: {track}"
            try:
                stdscr.addstr(status_y, 2, msg)
            except curses.error:
                pass
        stdscr.refresh()

    def animate_path(self, stdscr, path):
        """Renders the solution one step at a time."""
        if not path:
            return
        for i in range(1, len(path) + 1):
            self.render(stdscr, path[:i])
            curses.napms(50)  # 50ms delay per banana

    def run(self, stdscr):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            init_track = os.path.join("music", self.engine.playlist[0])
            pygame.mixer.music.load(init_track)
        except Exception:
            pass

        try:
            curses.start_color()
            curses.use_default_colors()
            if curses.has_colors():
                curses.init_pair(1, curses.COLOR_YELLOW, -1)
                curses.init_pair(2, curses.COLOR_MAGENTA, -1)
        except curses.error:
            pass

        stdscr.keypad(True)
        try:
            curses.curs_set(0)
        except curses.error:
            pass

        show_sol = False

        while True:
            cur_pos = tuple(self.engine.player_pos)
            path = self.engine.maze.solve(cur_pos, self.engine.exit)
            self.render(stdscr, path if show_sol else None)

            key = stdscr.getch()

            if key in (ord('q'), ord('Q'), 27):
                break

            # Music Toggle & Track Switch
            if key in (ord('m'), ord('M')):
                if self.engine.music_playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.play(-1)
                self.engine.music_playing = not self.engine.music_playing
            elif key == curses.KEY_RIGHT:
                self.engine.switch_music()

            # Mode Controls
            elif key in (ord('p'), ord('P')):
                self.engine.play_mode = not self.engine.play_mode
            elif key in (ord('s'), ord('S')):
                show_sol = not show_sol
                if show_sol:
                    self.animate_path(stdscr, path)
            elif key in (ord('r'), ord('R')):
                self.engine.regenerate()
                show_sol = False

            # Movement (Play Mode Only)
            if self.engine.play_mode and key in (
                curses.KEY_UP, curses.KEY_DOWN,
                curses.KEY_LEFT, curses.KEY_RIGHT
            ):
                res = self.engine.handle_move(key)
                if res == "COLLISION":
                    self.engine.health -= 1
                    if self.engine.health <= 0:
                        self.engine.regenerate()
                        self.engine.health = 3
                elif res == "WIN":
                    self.engine.regenerate()