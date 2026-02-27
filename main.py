from Ascii_render import AsciiRenderer
from mazegenerator import MazeGenerator

import curses

def main(stdscr):
    maze = MazeGenerator(width=20, height=10, seed=42)
    maze.generate()

    entry = (0, 0)
    exit = (maze.height - 1, maze.width - 1)

    renderer = AsciiRenderer(maze, entry, exit)
    renderer.run(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)