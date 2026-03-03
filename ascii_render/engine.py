import os
import pygame
import curses


class GameEngine:
    def __init__(self, maze, entry, exit_pos, playlist):
        self.maze = maze
        self.entry = entry
        self.exit = exit_pos
        self.player_pos = list(entry)
        self.score = 0
        self.health = 3
        self.play_mode = False
        self.music_playing = False
        self.music_index = 0
        self.playlist = playlist

    def switch_music(self):
        try:
            self.music_index = (self.music_index + 1) % len(self.playlist)
            track = self.playlist[self.music_index]
            track_path = os.path.join("music", track)
            pygame.mixer.music.load(track_path)
            if self.music_playing:
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def handle_move(self, direction):
        x, y = self.player_pos
        val = self.maze.grid[y][x]
        move_map = {
            curses.KEY_UP: (0, -1, 1),
            curses.KEY_RIGHT: (1, 0, 2),
            curses.KEY_DOWN: (0, 1, 4),
            curses.KEY_LEFT: (-1, 0, 8)
        }
        if direction not in move_map:
            return False

        dx, dy, wall_bit = move_map[direction]
        nx, ny = x + dx, y + dy

        has_wall = (val & wall_bit) != 0
        is_blocked = (
            0 <= nx < self.maze.width and
            0 <= ny < self.maze.height and
            self.maze.grid[ny][nx] == 15
        )

        if not has_wall and not is_blocked:
            self.player_pos = [nx, ny]
            if tuple(self.player_pos) == self.exit:
                self.score += 10
                if self.health < 3:
                    self.health += 1
                return "WIN"
            return "MOVED"
        return "COLLISION"

    def regenerate(self):
        w, h = self.maze.width, self.maze.height
        self.maze.grid = [[0xF for _ in range(w)] for _ in range(h)]
        self.maze.visited = [[False for _ in range(w)] for _ in range(h)]
        if hasattr(self.maze, 'apply_42_logo'):
            self.maze.apply_42_logo()
        self.maze.generate(self.entry[0], self.entry[1])
        self.player_pos = list(self.entry)