# src/dlmv/utils/text_renderer.py

import curses as c
import os

shortcuts = [
    ('h / ←',           "exit folder (cd ..)"),
    ('l / → / enter',   "open folder (cd foo/)"),
    ('k/j / ↑/↓',       "up/down"),
    ('c',               "clone"),
    ('p',               "custom path"),
    ('q',               "quit")
]

# TODO: [ ] BUG: draw_shortcuts(width) rendering on FileNavigator curses window.
def draw_shortcuts(window, width):
    """
    Draws shortcut descriptions in the top right corner.

    Parameters:
        window: The main window object provided by curses.
        shortcuts: A list of tuples containing shortcut keys and descriptions.
    """
    box_w = 30
    box_y, box_x = 1, width - box_w  # align top right with padding

    for idx, (key, desc) in enumerate(shortcuts):
        window.addstr(box_y + idx, box_x, f"{key}: {desc}")

# TODO: [ ] BUG: display_error(stdscr, message, height) not rendering errors from FileNavigator.
def display_error(stdscr, message, height):
    """
    Displays an error message on the screen.

    Parameters:
        stdscr: The main window object provided by curses.
        message: The error message to be displayed.
        height: The height of the terminal window.
    """
    y, x = stdscr.getyx()

    # Move to the error message position, clear the line, and display the error
    stdscr.move(height - 2, 1)
    stdscr.clrtoeol()
    stdscr.addstr(message, c.A_REVERSE)
    stdscr.refresh()
    c.napms(2000)  # Pause for 2 seconds to let the user read the message

    # Clear the error message
    stdscr.move(height - 2, 1)
    stdscr.clrtoeol()

    # Restore the original cursor position
    stdscr.move(y, x)
    stdscr.refresh()

def display_list(window, idx, scroll_pos, files, curr_path):
    """
    Display list of files in the window, with directories and files colored differently.

    Parameters:
        window (curses.window): The window object where files will be displayed.
        idx (int): The current selected index in the file list.
        scroll_pos (int): The current scroll position in the file list.
        files (list): A list of file names to be displayed.
        curr_path (str): The current path to resolve full paths for files/directories.

    """
    for i, file in enumerate(files):
        is_dir = os.path.isdir(os.path.join(curr_path, file))
        color_pair = 1 if is_dir else 2  # color pair 1 for dirs, 2 for files

        if idx == scroll_pos + i:
            window.addstr(i + 1, 1, file, c.color_pair(color_pair) | c.A_REVERSE)
        else:
            window.addstr(i + 1, 1, file, c.color_pair(color_pair))
