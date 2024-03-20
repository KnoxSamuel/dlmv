# src/utils/file_navigator.py

import os
import curses
from curses.textpad import Textbox, rectangle
from .key_mappings import _key_press
from .text_renderer import draw_shortcuts, display_error, display_list

class FileNavigator:
    """
    The FileNavigator class provides functionality to navigate through files and directories in
    a terminal-based user interface (TUI). It allows the user to view and interact with files
    and directories, including changing directories, opening folders, cloning, and more.

    Attributes:
        stdscr (curses.window): The standard screen window.
        cloney_is (None or str): The cloney_is value.
        curr_path (str): The current path.
        idx (int): The index.
        files (list): The list of files in the current path.
        h (int): The height of the screen.
        w (int): The width of the screen.
        window (curses.window): The window object.
        scroll_pos (int): The scroll position.
        shortcuts (list): The list of shortcuts.

    Methods:
        __init__(self, stdscr, cloney_is=None): Initializes a new FileNavigator object.
        update_files(self): Updates the list of files in the current path.
        create_window(self): Creates a new window using the curses library.
        render(self): Renders the file navigator screen.
        prep_screen(self): Prepares the screen for display.
        is_terminal_small(self): Checks if the terminal window is too small for the interface.
        get_curr_path(self): Displays the current path above the border and visible files.
        get_visible_files(self): Retrieves the list of visible files based on the scroll position.
        refresh(self): Refreshes the terminal and window.
        validate_path(self, path): Validates if the given path exists and is a directory.
        get_custom_path(self): Prompts user for custom destination path.
        navigate(self): Main loop for rendering the files TUI and handling user input.
    """

    def __init__(self, stdscr, cloney_is=None):
        """
        Initializes a FileNavigator object.

        Parameters:
            stdscr (curses.window): the standard screen window.
            cloney_is (None or str): value of cloney_is.
        """
        self.stdscr = stdscr
        self.cloney_is = cloney_is
        self.curr_path = os.getcwd()
        self.idx = 0
        self.update_files()
        self.h, self.w = stdscr.getmaxyx()
        self.window = self.create_window()
        self.scroll_pos = 0

    def update_files(self):
        """
        Updates self.files with the list of files in the current path.
        """
        self.files = os.listdir(self.curr_path)

    def create_window(self):
        """
        Creates a new window using the curses library.

        Returns:
            window (curses.window): The newly created window.
        """
        window = curses.newwin(self.h - 2, self.w - 2, 1, 1)
        return window

    def render(self):
        """
        Renders the file navigator screen.

        Prepares render, shows files, draws shortcuts, and refreshes display.
        """
        self.prep_screen()
        self.get_curr_path()
        draw_shortcuts(self.w)
        self.refresh()

    def prep_screen(self):
        """
        Prepares the screen for display.

        If the terminal size is too small, it displays an error message.
        Otherwise, it clears the standard screen and window, and draws a box.
        """
        if self.is_terminal_small():
            display_error(self.stdscr, 'Terminal too small!!', self.h)

        else:
            self.stdscr.clear()
            self.window.clear()
            self.stdscr.box()

    def is_terminal_small(self):
        """
        Check if the terminal window is too small to display the interface.

        Returns:
            bool: True if the terminal window is too small, False otherwise.
        """
        return self.h < 4 or self.w < 20

    def get_curr_path(self):
        """
        Display the current path above border.

        This method adds the current path to the top border.
        It also retrieves visible files and renders with `display_list`.
        """
        self.stdscr.addstr(0, 1, f" -> Path: {self.curr_path} ", curses.A_REVERSE)
        visible_files = self.get_visible_files()
        display_list(self.window, self.idx, self.scroll_pos, visible_files, self.curr_path)

    def get_visible_files(self):
        """
        Updates the list of files that based on the scroll position.

        Returns:
            list: A list of files that should be visible.
        """
        return self.files[self.scroll_pos:self.scroll_pos + self.h - 4]

    def refresh(self):
        """
        Refresh terminal and window.

        This method updates the display to reflect any changes made.
        """
        self.stdscr.refresh()
        self.window.refresh()

    def validate_path(self, path):
        """
        Validates if the given path exists and is a directory.

        Parameters:
            path (str): The path to be validated.

        Returns:
            bool: True if the path exists and is a directory, False otherwise.
        """
        expanded_path = os.path.expanduser(path)
        return os.path.exists(expanded_path) and os.path.isdir(expanded_path)

    def get_custom_path(self):
        """
        Prompts the user to enter a custom destination path and updates the current path if valid.
        """
        input_w = 40
        input_h = 1

        win_w = self.window.getmaxyx()[1]
        box_x = (win_w - input_w) // 2
        box_y = 3
        msg = "Destination path: "

        input_win = curses.newwin(input_h+2, input_w, box_y, box_x)
        self.stdscr.addstr(box_y-1, box_x, msg)
        rectangle(self.stdscr, box_y-1, box_x-1, box_y+input_h+1, box_x+input_w+1)
        self.stdscr.refresh()

        box = Textbox(input_win)
        box.edit()
        input_win.refresh()

        path = box.gather().strip()
        expanded_path = os.path.expanduser(path)

        if self.validate_path(expanded_path):
            self.curr_path = expanded_path
            self.update_files()
            self.idx = 0
            self.window.clear()
            self.render()
        else:
            display_error(self.stdscr, "Invalid path...", self.h)

        self.stdscr.touchwin()
        self.refresh()

    def navigate(self):
        """
        Main loop for rendering the files TUI and handling of user input.

        Listens for input to update the TUI, quitting when `q` is received.
        """
        while True:
            self.render()
            key = self.stdscr.getch()
            _key_press(key, self)
            if curses.isendwin():
                break

