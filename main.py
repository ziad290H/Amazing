from sys import argv
import curses
from parsing import Parser
from mazegenerator import MazeGenerator
from Ascii_render import AsciiRenderer
from intro import play_intro

def main(stdscr, config):
    # Hide the cursor for better visuals
    play_intro(stdscr)
    curses.curs_set(0) 
    
    maze = MazeGenerator(
        width=config["WIDTH"], 
        height=config["HEIGHT"], 
        seed=config.get("SEED")
    )
    maze.apply_42_logo()
    # Start generation at the entry point
    maze.generate(config["ENTRY"][0], config["ENTRY"][1])

    renderer = AsciiRenderer(maze, config["ENTRY"], config["EXIT"])
    
    # This now enters the while loop
    renderer.run(stdscr)

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