import os
import pygame
import curses
from typing import List, Tuple, Union, Any


class GameEngine:
    """Manages the internal game state, player movement, and audio logic.

    This class serves as the bridge between the raw maze data and the
    user interface, tracking player health, position, and music state.

    Attributes:
        maze (MazeGenerator): The current maze instance being played.
        entry (tuple): The (x, y) coordinates where the player starts.
        exit (tuple): The (x, y) coordinates of the finish line.
        player_pos (list): Current [x, y] coordinates of the player.
        score (int): The current player score.
        health (int): Remaining lives before a forced regeneration.
        play_mode (bool): Toggle for manual movement mode.
        music_playing (bool): Current toggle state of the background audio.
        playlist (list): List of filenames for the music tracks.
        music_index (int): Index of the currently active music track.
    """

    def __init__(
        self,
        maze: Any,
        entry: Tuple[int, int],
        exit_pos: Tuple[int, int],
        playlist: List[str]
    ) -> None:
        """Initializes the GameEngine with maze data and player state.

        Args:
            maze (MazeGenerator): The maze object containing the grid logic.
            entry (tuple): The starting (x, y) position for the player.
            exit_pos (tuple): The target (x, y) position for victory.
            playlist (list): A list of strings representing audio filenames.
        """
        self.maze = maze
        self.entry = entry
        self.exit = exit_pos
        self.player_pos: List[int] = list(entry)
        self.score: int = 0
        self.health: int = 3
        self.play_mode: bool = False
        self.music_playing: bool = False
        self.music_index: int = 0
        self.playlist: List[str] = playlist

    def switch_music(self) -> None:
        """Cycles to the next track in the playlist
         and updates the audio mixer.

        Increments the music_index and attempts to load and play the new track.
        If music_playing is True, the new track starts immediately.
        """
        try:
            self.music_index = (self.music_index + 1) % len(self.playlist)
            track = self.playlist[self.music_index]
            track_path = os.path.join("music", track)
            pygame.mixer.music.load(track_path)
            if self.music_playing:
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def handle_move(self, direction: int) -> Union[str, bool]:
        """Processes player movement based on input and maze wall logic.

        Checks the bitmask of the current cell to see if a wall exists in the
        requested direction and ensures the target cell is not a 'blocked'
        logo cell.

        Args:
            direction (int): The curses key code for the movement direction.

        Returns:
            Union[str, bool]: "WIN" if player reaches exit, "MOVED" if success,
                "COLLISION" if blocked. Returns False if direction is invalid.
        """
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

    def regenerate(self) -> None:
        """Resets the game state with a new randomly generated maze.

        Instantiates a new MazeGenerator, re-applies the '42' logo,
        fully carves the paths, and resets the player to the entry point.
        """
        from mazegen.mazegenerator import MazeGenerator
        self.maze = MazeGenerator(self.maze.width, self.maze.height)
        self.maze.apply_42_logo()
        list(self.maze.generate(self.entry[0], self.entry[1]))
        self.player_pos = list(self.entry)
