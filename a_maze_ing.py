import sys
import curses
import time
from typing import Any, Dict
from parsing import Parser
from mazegenerator import MazeGenerator
from ascii_render import AsciiRenderer
from intro import play_intro
from hexadecimale import HexEncoder


def main(stdscr: Any, config: Dict[str, Any]) -> None:
    """Orchestrates the maze generation, animation, and game loop.

    Handles the initialization of game components, player character selection,
    real-time generation animation, and the final state encoding to a file.

    Args:
        stdscr: The main curses window object.
        config (Dict[str, Any]): Dictionary containing configuration parameters
            such as dimensions, entry/exit points, and file paths.
    """
    # Capture the emoji chosen by the user
    player_emoji = play_intro(stdscr)

    curses.curs_set(0)

    maze = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        seed=config.get("SEED")
    )

    renderer = AsciiRenderer(
        maze, config["ENTRY"], config["EXIT"], player_emoji, config
    )

# Initialize the colors before animating
    maze.apply_42_logo()
    # Animate maze generation
    for _ in maze.generate(config["ENTRY"][0], config["ENTRY"][1]):
        renderer.render(stdscr)
        stdscr.refresh()
        time.sleep(0.02)


    solution_path = maze.solve(config["ENTRY"], config["EXIT"])
    encoder = HexEncoder(
        maze.grid,
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
        solution_path
    )

    try:
        with open(config["OUTPUT_FILE"], "w") as f:
            f.write(encoder.encode())
    except PermissionError:
        raise PermissionError(
            f"You Dont have the Permissions of the file {config['OUTPUT_FILE']}"
        )

    # Start the interactive game loop
    renderer.run(stdscr)

    # Reset terminal background and clear screen on exit
    stdscr.bkgd(' ', curses.color_pair(0))
    stdscr.clear()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py config.txt")
        sys.exit(1)

    try:
        parser = Parser(sys.argv[1])
        config_data = parser.parse()
        curses.wrapper(main, config_data)
    except Exception as e:
        print(f"Fatal Error: {e}")