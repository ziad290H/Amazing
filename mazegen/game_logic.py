from typing import Any, List, Tuple


class GameEngine:
    """Manages the internal game state, player movement, and win/loss logic.

    This class tracks the player's position within the maze grid, manages
    scoring and health, and evaluates movement against bitmask-encoded walls.

    Attributes:
        maze (Any): The maze object containing the grid bitmask data.
        player_pos (List[int]): Current [y, x] coordinates of the player.
        exit_pos (Tuple[int, int]): The [y, x] coordinates of the goal.
        score (int): The current player score.
        health (int): Remaining lives before game over.
        game_over (bool): Flag indicating if the player has lost.
    """

    def __init__(
        self,
        maze: Any,
        entry: Tuple[int, int],
        exit_pos: Tuple[int, int]
    ) -> None:
        """Initializes the GameEngine with maze data and player state.

        Args:
            maze (Any): The maze generator or grid object.
            entry (Tuple[int, int]): Starting coordinates for the player.
            exit_pos (Tuple[int, int]): Goal coordinates for the player.
        """
        self.maze: Any = maze
        self.player_pos: List[int] = list(entry)  # [y, x]
        self.exit_pos: Tuple[int, int] = exit_pos
        self.score: int = 0
        self.health: int = 3
        self.game_over: bool = False

    def move(self, direction: str) -> None:
        """Processes player movement using bitwise wall detection.

        Checks the current cell value against a bitmask (1: North, 2: South,
        4: East, 8: West) to determine if a move is valid.

        Args:
            direction (str): The requested movement
            ('UP', 'DOWN', 'LEFT', 'RIGHT').
        """
        y, x = self.player_pos
        cell_val = self.maze.grid[y][x]

        # Bitwise checks for walls (1: North, 2: South, 4: East, 8: West)
        if direction == 'UP':
            if not (cell_val & 1):
                self.player_pos[0] -= 1
            else:
                self.take_damage()
        elif direction == 'DOWN':
            if not (cell_val & 2):
                self.player_pos[0] += 1
            else:
                self.take_damage()
        elif direction == 'RIGHT':
            if not (cell_val & 4):
                self.player_pos[1] += 1
            else:
                self.take_damage()
        elif direction == 'LEFT':
            if not (cell_val & 8):
                self.player_pos[1] -= 1
            else:
                self.take_damage()

        # Check Win Condition
        if tuple(self.player_pos) == self.exit_pos:
            self.win_round()

    def take_damage(self) -> None:
        """Decrements player health and checks for game over state."""
        self.health -= 1
        if self.health <= 0:
            self.game_over = True

    def win_round(self) -> None:
        """Updates score and health upon reaching
                the exit and triggers a reset."""
        self.score += 1
        if self.health < 3:
            self.health += 1  # Restore heart on win
        # Signal for regeneration
        self.reset_player()

    def reset_player(self) -> None:
        """Resets the player position to the entry point.

        Note: Entry is usually provided as (x, y) in config but stored as
        [y, x] for grid indexing.
        """
        pass
