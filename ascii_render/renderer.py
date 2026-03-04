import curses
import pygame
import os
from typing import Any, List, Optional, Tuple
from .engine import GameEngine
from .view import MazeView


class AsciiRenderer:
    """Handles the visual representation of the maze using the Curses library.

    Attributes:
        engine (GameEngine): The logic controller for player movement and state.
        player_char (str): The emoji or character representing the player.
        config (Optional[dict]): Configuration data for the game.
    """

    def __init__(
        self,
        maze: Any,
        entry: Tuple[int, int],
        exit_pos: Tuple[int, int],
        char: str = "🐒",
        config: Optional[dict] = None
    ) -> None:
        """Initializes the AsciiRenderer with game logic and visual settings.

        Args:
            maze (MazeGenerator): The generated maze object to be displayed.
            entry (tuple): The (x, y) starting coordinates for the player.
            exit_pos (tuple): The (x, y) coordinates of the goal.
            char (str, optional): Character representing the player.
                Defaults to "🐒".
            config (dict, optional): Data from the configuration file.
                Defaults to None.
        """
        playlist: List[str] = [
            "saha.mp3", "Dance_it_out.mp3", "joy_to_the_world.mp3",
            "game_over.mp3", "summer_joy.mp3"
        ]
        self.engine: GameEngine = GameEngine(maze, entry, exit_pos, playlist)
        self.player_char: str = char
        self.config: Optional[dict] = config

    def render(
        self,
        stdscr: Any,
        path: Optional[List[Tuple[int, int]]] = None,
        them: int =1
    ) -> None:
        """Draws the current state of the game, HUD, and music status.

        Args:
            stdscr: The main curses window object used for drawing.
            path (list, optional): A list of (x, y) tuples to highlight
                as the solution path. Defaults to None.
        """
        try:
            curses.start_color()
            curses.use_default_colors()

            # Pair 1: Cyan Walls
            curses.init_pair(1, curses.COLOR_CYAN, -1)
            # Pair 2: Blue Logo
            curses.init_pair(2, curses.COLOR_BLUE, -1)
            # Pair 3: Green Walls (New!)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
        except curses.error:
            pass      
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()
        path_set = set(path) if path else set()

        MazeView.draw_hud(stdscr, self.engine)
        MazeView.draw_maze(stdscr, self.engine, path_set, self.player_char,
                                                        them)
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

    def animate_path(self, stdscr: Any, path: List[Tuple[int, int]]) -> None:
        """Visually animates the solution path step-by-step.

        Args:
            stdscr: The main curses window object.
            path (list): The ordered list of coordinates to animate.
        """
        if not path:
            return
        for i in range(1, len(path) + 1):
            self.render(stdscr, path[:i])
            curses.napms(50)  # 50ms delay per step

    def run(self, stdscr: Any) -> None:
        """Starts the main game loop and handles key inputs.

        Args:
            stdscr: The main curses window object.
        """
        # --- INITIALIZATION ---
        show_sol = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            init_track = os.path.join("music", self.engine.playlist[0])
            pygame.mixer.music.load(init_track)
        except Exception:
            pass

        stdscr.keypad(True)
        try:
            curses.curs_set(0)
        except curses.error:
            pass
        
        # State variable for toggling solution visibility
        them_idx = 1
        show_sol = False

        # --- MAIN GAME LOOP ---
        while True:
            # 1. Update logic: Always get a fresh path from current position to exit
            px, py = self.engine.player_pos
            ex, ey = self.engine.exit
            cur_pos = (int(px), int(py))
            exit_pos = (int(ex), int(ey))
            # Note: Ensure your solver expects (x, y) or [y, x] consistently
            path = self.engine.maze.solve(cur_pos, exit_pos)
            if not path:
                message = f"No path from {cur_pos} to {exit_pos}\n"
            else:
                message = f"we have the path {path}"
            with open("debug.log", "a") as f:
                    f.write(f"path from {cur_pos} to {exit_pos}\n, path:{path}")
            # 2. Render current frame
            self.render(stdscr, path if show_sol else None, them=them_idx)

            # 3. Input Handling
            key = stdscr.getch()

            if key in (ord('q'), ord('Q'), 27):  # Quit
                break

            # Music Toggle & Track Switch
            if key in (ord('m'), ord('M')):
                if self.engine.music_playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.play(-1)
                self.engine.music_playing = not self.engine.music_playing
            
            elif key == curses.KEY_RIGHT and not self.engine.play_mode:
                # Only switch music via Right Arrow if not in movement mode
                self.engine.switch_music()

            # Mode Controls
            elif key in (ord('p'), ord('P')):
                self.engine.play_mode = not self.engine.play_mode
            
            elif key in (ord('s'), ord('S')):
                show_sol = not show_sol
                if show_sol and path:
                    # Trigger the animation sequence if showing the path
                    self.animate_path(stdscr, path)
            
            elif key in (ord('r'), ord('R')):
                self.engine.regenerate()
                show_sol = False  # Reset solution view on new maze
            elif key in (ord('c'), ord('C')):
                them_idx = (them_idx + 1) % 3

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
                    show_sol = False