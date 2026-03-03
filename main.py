from sys import argv
import curses
from parsing import Parser
from mazegenerator import MazeGenerator
from Ascii_render import AsciiRenderer
from intro import play_intro
from hexadecimale import HexEncoder

def main(stdscr, config):
    # Capture the emoji chosen by the user
    player_emoji = play_intro(stdscr)
    
    curses.curs_set(0) 
    
    maze = MazeGenerator(
        width=config["WIDTH"], 
        height=config["HEIGHT"], 
        seed=config.get("SEED")
    )
    solution_path = maze.solve(config["ENTRY"], config["EXIT"])
    encoder = HexEncoder(
        grid=maze.grid, # Ensure this matches the object structure HexEncoder expects
        width=config["WIDTH"],
        height=config["HEIGHT"],
        entry=config["ENTRY"],
        exit=config["EXIT"],
        path=solution_path
    )
    with open(config["OUTPUT_FILE"], "w") as f:
        f.write(encoder.encode())

    maze.apply_42_logo()
    maze.generate(config["ENTRY"][0], config["ENTRY"][1])

    # Pass player_emoji to the renderer
    renderer = AsciiRenderer(maze, config["ENTRY"], config["EXIT"], player_emoji, config_data)
    renderer.run(stdscr)
    # This forces the entire terminal background to match Color Pair 1
    stdscr.bkgd(' ', curses.color_pair(0)) 
    stdscr.clear()

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python3 main.py config.txt")
        exit(1)

    try:
        parser = Parser(argv[1])
        config_data = parser.parse()
        curses.wrapper(main, config_data)
    except Exception as e:
        print(f"Fatal Error: {e}")