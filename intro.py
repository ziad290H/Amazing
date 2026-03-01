import time
import curses

def play_intro(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    sh, sw = stdscr.getmaxyx()
    
    title = "PROJECT AMAZING"
    subtitle = "Initializing Jungle Protocol...🐒"
    authors = "made by Zdaouari && momahdam"
    loading_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    ask_expl = "do you want an explainition for the game?\n\n \t\t please enter 'Y' or 'N' to confirm!"
    for i in range(len(authors)):
        stdscr.erase()
        stdscr.addstr(sh//3 - 1, (sw - len(authors))//2, authors, curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.05)
    # 1. Typewriter Subtitle
    for i in range(len(subtitle) + 1):
        stdscr.erase()
        # Center the title
        stdscr.addstr(sh//2 - 1, (sw - len(title))//2, title, curses.A_BOLD)
        # Type the subtitle
        stdscr.addstr(sh//2 + 1, (sw - len(subtitle))//2, subtitle[:i])
        stdscr.refresh()
        time.sleep(0.05)

    # 2. Spinning Loader
    for i in range(20):
        char = loading_chars[i % len(loading_chars)]
        stdscr.addstr(sh//2 + 3, sw//2, char)
        stdscr.refresh()
        time.sleep(0.1)
        
    for i in ask_expl:
        stdscr.erase()
        stdscr.addstr(sh//2 - 1, (sw - len(ask_expl))//2, ask_expl, curses.A_BOLD)
        stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('Y') or key == ord('y'):
            stdscr.erase()
            msg = "mn b3d w nchr7o"
            sh, sw = stdscr.getmaxyx()
            stdscr.addstr(sh // 2, (sw - len(msg)) // 2, msg, curses.A_BOLD)
            stdscr.refresh()

            # Hold the screen for 4 seconds
            time.sleep(4)
            break
        elif key == ord('N') or key == ord('n'):
            stdscr.erase()
            msg = "OKey lets start playing"
            sh, sw = stdscr.getmaxyx()
            stdscr.addstr(sh // 2, (sw - len(msg)) // 2, msg, curses.A_BOLD)
            stdscr.refresh()

            # Hold the screen for 4 seconds
            time.sleep(4)
            break

    stdscr.clear()
    stdscr.refresh()