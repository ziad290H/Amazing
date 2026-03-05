import time
import curses
from typing import List


def get_instructions() -> List[str]:
    """Returns the mission briefing and control instructions for the game.

    Returns:
        List[str]: A list of strings, each representing a line of instructions.
    """
    return [
        "--- JUNGLE PROTOCOL: MISSION BRIEFING ---",
        "",
        "GOAL: Reach the Coconut (🥥) or Flower (🌸) to score points.",
        "DANGER: Hitting walls reduces Health (❤️ ). 0 Health = Game Over.",
        "",
        "CONTROLS:",
        " [P] PLAY/STOP - Toggle between Free-Look and Control Mode.",
        " [Arrows]      - Move your character through the jungle.",
        " [S] SOLVE      - Toggle the shortest path visualization.",
        " [R] GENERATE   - Create a brand new random maze layout.",
        "",
        "CUSTOMIZATION:",
        " [T] WALL THEME - Cycle colors for the maze boundaries.",
        " [C] ICON COLOR - Change the color of the Monkey and Exit.",
        " [M] MUSIC      - Turn the jungle soundtrack ON/OFF.",
        " [→] NEXT SONG  - Skip to the next track in the playlist.",
        "",
        "NOTE: The '42' pattern is encoded in the jungle's DNA.",
        "It will always remain RED regardless of the Wall Theme.",
        "",
        "--- PRESS [Y] AGAIN TO RETURN TO THE JUNGLE ---"
    ]


def play_intro(stdscr: curses.window) -> str:
    """Executes the game's introductory sequence and character selection.

    This includes a typewriter effect for titles, a loading animation,
    an optional instruction screen, and a visual character picker.

    Args:
        stdscr (curses.window): The main curses window object.

    Returns:
        str: The emoji representing the chosen character ("🐒" or "🐇").
    """
    #It represents your entire terminal window.
    # make the curseur dont appear in screen
    curses.curs_set(0)
    # wiped the teminal window completly and make it refresh
    stdscr.clear()
    # get the height and width of the screen
    sh, sw = stdscr.getmaxyx()

    title = "PROJECT AMAZING"
    subtitle = "Initializing Jungle Protocol...🐒"
    authors = "made by z.daouari && mo.mahdam"
    loading_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    # 1. Authors Typewriter
    for i in range(len(authors) + 1):
        # clear the terminale
        stdscr.erase()
        stdscr.addstr(sh // 3, (sw - len(authors)) // 2, authors[:i],
                      curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.05)
    time.sleep(0.5)

    # 2. Title & Subtitle Typewriter
    for i in range(len(subtitle) + 1):
        # delet everything that is already in the screen
        stdscr.erase()
        stdscr.addstr(
                    sh // 2 - 1,
                    (sw - len(title)) // 2,
                    title, curses.A_BOLD
            )
        stdscr.addstr(sh // 2 + 1, (sw - len(subtitle)) // 2, subtitle[:i])
        stdscr.refresh()
        time.sleep(0.05)

    # 3. Spinning Loader
    for i in range(20):
        char = loading_chars[i % len(loading_chars)]
        stdscr.addstr(sh // 2 + 3, sw // 2, char)
        #reveal the output
        stdscr.refresh()
        time.sleep(0.1)

    # 4. Explanation Prompt
    stdscr.erase()
    ask_expl = "Do you want an explanation for the game? (Y/N)"
    stdscr.addstr(sh // 2, (sw - len(ask_expl)) // 2, ask_expl, curses.A_BOLD)
    #reveal the output
    stdscr.refresh()

    while True:
        #getch make the screen pose untile you press a key
        key = stdscr.getch()
        if key in [ord('Y'), ord('y')]:
            stdscr.erase()
            explanation = get_instructions()
            for idx, line in enumerate(explanation):
                stdscr.addstr(sh // 2 - 4 + idx, (sw - len(line)) // 2, line)
            stdscr.refresh()
            stdscr.getch()
            break
        elif key in [ord('N'), ord('n')]:
            break

    # 5. Character Selection
    char1_icon = [["🌿", "🌿", "🌿"], ["🌿", "🐒", "🌿"], ["🌿", "🌿", "🌿"]]
    char2_icon = [["🌸", "🥕", "🌸"], ["🥕", "🐇", "🥕"], ["🌸", "🥕", "🌸"]]

    chosen_char = "🐒"

    while True:
        stdscr.erase()
        prompt = "CHOOSE YOUR CHARACTER"
        stdscr.addstr(sh // 4, (sw - len(prompt)) // 2, prompt,
                      curses.A_UNDERLINE)

        # Draw Option 1 (Monkey)
        stdscr.addstr(sh // 2 - 2, sw // 3 - 5, "1. MONKEY")
        for idx, row in enumerate(char1_icon):
            stdscr.addstr(sh // 2 + idx, sw // 3 - 5, "".join(row))

        # Draw Option 2 (Rabbit)
        stdscr.addstr(sh // 2 - 2, (2 * sw // 3) - 5, "2. RABBIT")
        for idx, row in enumerate(char2_icon):
            stdscr.addstr(sh // 2 + idx, (2 * sw // 3) - 5, "".join(row))

        stdscr.addstr(sh - 2, (sw - 25) // 2, "Press '1' or '2' to start")
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('1'):
            chosen_char = "🐒"
            break
        elif key == ord('2'):
            chosen_char = "🐇"
            break

    # Transition Message
    stdscr.erase()
    final_msg = f"Starting adventure with {chosen_char}!"
    stdscr.addstr(
        sh // 2,
        (sw - len(final_msg)) // 2,
        final_msg, curses.A_BOLD
        )
    stdscr.refresh()
    time.sleep(2)

    return chosen_char
