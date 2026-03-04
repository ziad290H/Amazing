import sys
import curses
from parsing import Parser
from mazegenerator import MazeGenerator
from ascii_render import AsciiRenderer
from intro import play_intro
from hexadecimale import HexEncoder
import time


def main(stdscr, config):
    # Capture the emoji chosen by the user
    player_emoji = play_intro(stdscr)

    curses.curs_set(0)

    maze = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        seed=config.get("SEED")
    )
    renderer = AsciiRenderer(
        maze, config["ENTRY"], config["EXIT"], player_emoji, config_data
        )

    for i in maze.generate(config["ENTRY"][0], config["ENTRY"][1]):
        renderer.render(stdscr)
        stdscr.refresh()
        time.sleep(0.02)

    maze.apply_42_logo()

    solution_path = maze.solve(config["ENTRY"], config["EXIT"])
    encoder = HexEncoder(
        maze.grid,
        # Ensure this matches the object structure HexEncoder expects
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
            "You Dont have the Permissions"
            f"of the file {config['OUTPUT_FILE']}"
        )
        sys.exit(1)
    # Pass player_emoji to the renderer
    renderer.run(stdscr)
    # This forces the entire terminal background to match Color Pair 1
    stdscr.bkgd(' ', curses.color_pair(0)) 
    stdscr.clear()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py config.txt")
        exit(1)

    try:
        parser = Parser(sys.argv[1])
        config_data = parser.parse()
        curses.wrapper(main, config_data)
    except Exception as e:
        print(f"Fatal Error: {e}")
