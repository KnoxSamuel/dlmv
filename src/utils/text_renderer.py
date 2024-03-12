# src/utils/text_renderer.py

import curses
import os

shortcuts = [
    ('h / ←',           "exit folder (cd ..)"),
    ('l / → / enter',   "open folder (cd dir/)"),
    ('k/j / ↑/↓',       "scroll up/down"),
    ('c',               "clone"),
    ('p',               "custom path"),
    ('q',               "quit")
]

def draw_shortcuts(width):
    """
    Draws a box with shortcut descriptions in the top right corner.

    Parameters:
        stdscr: The main window object provided by curses.
        shortcuts: A list of tuples containing shortcut keys and descriptions.
        height: The height of the terminal window.
        width: The width of the terminal window.
    """
    box_h = len(shortcuts) + 2
    box_w = max(len(desc) for _, desc in shortcuts) + 4
    box_y, box_x = 1, width - box_w - 2  # align top right with padding
    
    keys_win = curses.newwin(box_h, box_w, box_y, box_x)
    keys_win.box()
    
    for idx, (key, desc) in enumerate(shortcuts):
        keys_win.addstr(idx + 1, 2, f"{key}: {desc}")
    keys_win.refresh()

def display_list(window, idx, scroll_pos, files):
    """
    Display the list of files in the window.

    Parameters:
        window (curses.window): The window object where files will be displayed.
        idx (int): The current selected index in the file list.
        scroll_pos (int): The current scroll position in the file list.
        files (list): A list of file names to be displayed.
    """
    for i, file in enumerate(files):
        if idx == scroll_pos + i:
            window.addstr(i+1, 1, file, curses.A_REVERSE)
        else:
            window.addstr(i+1, 1, file)

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
    stdscr.addstr(message, curses.A_REVERSE)
    stdscr.refresh()
    curses.napms(2000)  # Pause for 2 seconds to let the user read the message

    # Clear the error message
    stdscr.move(height - 2, 1)
    stdscr.clrtoeol()

    # Restore the original cursor position
    stdscr.move(y, x)
    stdscr.refresh()
