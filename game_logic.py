import curses

class GameEngine:
    def __init__(self, maze, entry, exit_pos):
        self.maze = maze
        self.player_pos = list(entry) # [y, x]
        self.exit_pos = exit_pos
        self.score = 0
        self.health = 3
        self.game_over = False

    def move(self, direction):
        """ direction: 'UP', 'DOWN', 'LEFT', 'RIGHT' """
        y, x = self.player_pos
        cell_val = self.maze.grid[y][x]

        # Bitwise checks for walls (1: North, 2: South, 4: East, 8: West)
        if direction == 'UP':
            if not (cell_val & 1): 
                self.player_pos[0] -= 1
            else: self.take_damage()
        elif direction == 'DOWN':
            if not (cell_val & 2): 
                self.player_pos[0] += 1
            else: self.take_damage()
        elif direction == 'RIGHT':
            if not (cell_val & 4): 
                self.player_pos[1] += 1
            else: self.take_damage()
        elif direction == 'LEFT':
            if not (cell_val & 8): 
                self.player_pos[1] -= 1
            else: self.take_damage()

        # Check Win Condition
        if tuple(self.player_pos) == self.exit_pos:
            self.win_round()

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.game_over = True

    def win_round(self):
        self.score += 1
        if self.health < 3:
            self.health += 1 # Restore heart on win
        # Signal for regeneration
        self.reset_player()

    def reset_player(self):
        # Entry is usually (x, y) in your config, but we use [y, x] for grid
        pass