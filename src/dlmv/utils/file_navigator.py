# src/dlmv/utils/file_navigator.py

import os
import curses
from curses.textpad import Textbox, rectangle
from .key_mappings import _key_press

class FileNavigator:
    """
    The FileNavigator class provides functionality to navigate through files and directories in
    a terminal-based user interface (TUI). It allows the user to view and interact with files
    and directories, including changing directories, opening folders, cloning, and more.

    Attributes:
        stdscr (curses.window): The standard screen window.
        cloney_instance (None or str): The cloney_instance value.
        curr_path (str): The current path.
        idx (int): The index.
        files (list): The list of files in the current path.
        h (int): The height of the screen.
        w (int): The width of the screen.
        window (curses.window): The window object.
        scroll_pos (int): The scroll position.
        shortcuts (list): The list of shortcuts.

    Methods:
        __init__(self, stdscr, cloney_instance=None): Initializes a new FileNavigator object.
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

    def __init__(self, stdscr, cloney_instance=None):
        """
        Initializes a FileNavigator object.

        Parameters:
            stdscr (curses.window): the standard screen window.
            cloney_instance (None or str): value of cloney_instance.
        """
        self.stdscr = stdscr
        self.cloney_instance = cloney_instance
        self.curr_path = os.getcwd()
        self.idx = 0
        self.update_files()
        self.h, self.w = stdscr.getmaxyx()
        self.window = self.create_window()
        self.scroll_pos = 0
        self.shortcuts = [
            ('h ←       ', "exit folder"),
            ('l → enter ', "open folder"),
            ('k|j ↑|↓   ', "up|down"),
            ('        c ', "clone"),
            ('        p ', "enter path"),
            ('        q ', "quit")
        ]

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

        Prepares render, shows files and shortcuts, and refreshes display.
        """
        self.prep_screen()
        self.get_curr_path()
        self.draw_shortcuts()
        visible_files = self.get_visible_files()
        self.display_list(self.idx, self.scroll_pos, visible_files, self.curr_path)
        self.refresh()

    def prep_screen(self):
        """
        Prepares the screen for display.

        If the terminal size is too small, it displays an error message.
        Otherwise, it clears the standard screen and window, and draws a box.
        """
        if self.is_terminal_small():
            self.display_error('Terminal too small!!')

        else:
            self.stdscr.clear()
            self.window.clear()
            self.stdscr.box()

    def refresh(self):
        """
        Refresh terminal and window.

        This method updates the display to reflect any changes made.
        """
        self.stdscr.refresh()
        self.window.refresh()

    def is_terminal_small(self):
        """
        Check if the terminal window is too small to display the interface.

        Returns:
            bool: True if the terminal window is too small, False otherwise.
        """
        return self.h < 20 or self.w < 40

    def get_curr_path(self):
        """
        This method displays the current path to the top border.

        """
        self.stdscr.addstr(0, 1, f" -> Path: {self.curr_path} ", curses.A_REVERSE)

    def get_visible_files(self):
        """
        Updates the list of files that based on the scroll position.

        Returns:
            list: A list of files that should be visible.
        """
        return self.files[self.scroll_pos:self.scroll_pos + self.h - 4]

    def draw_shortcuts(self):
        """
        Draws shortcut descriptions in the top right corner.

        """
        box_w = 25
        box_x = self.w - box_w - 1  # align top right with padding
        for idx, (key, desc) in enumerate(self.shortcuts):
            self.window.addstr(idx, box_x, f"{key}: {desc}")
        
    def display_list(self, idx, scroll_pos, files, curr_path):
        """
        Display list of files in the window, with directories and files colored differently.

        Parameters:

            idx (int): The current selected index in the file list.
            scroll_pos (int): The current scroll position in the file list.
            files (list): A list of file names to be displayed.
            curr_path (str): The current path to resolve full paths for files/directories.

        """
        for i, file in enumerate(files):
            is_dir = os.path.isdir(os.path.join(curr_path, file))
            color_pair = 1 if is_dir else 2  # color pair 1 for dirs, 2 for files
            if idx == scroll_pos + i:
                self.window.addstr(i + 1, 1, file, curses.color_pair(color_pair) | curses.A_REVERSE)
            else:
                self.window.addstr(i + 1, 1, file, curses.color_pair(color_pair))

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

    def display_error(self, message):
        """
        Displays an error message on the screen.

        Parameters:

            message: The error message to be displayed.
        """
        error_y = self.h // 4
        self.stdscr.addstr(error_y, 1, message, curses.A_REVERSE)
        self.stdscr.refresh()
        curses.napms(3000)  # Pause for 3 seconds to let the user read the message
        self.stdscr.move(error_y, 1)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

    def get_custom_path(self):
        """
        Prompts the user to enter a custom destination path and updates the current path if valid.
        
        If not, briefly displays an error before clearing the input and error text and giving control
        back to the main file navigate screen.
        """
        # Clear the window and prompt for a new path
        self.window.clear()
        prompt_msg = "Enter new path: "
        self.window.addstr(1, 1, prompt_msg)
        self.window.refresh()

        # Enable echo to get input from the user
        curses.echo()
        input_path = self.window.getstr(1, len(prompt_msg) + 1).decode('utf-8')
        curses.noecho()

        # Validate the input path
        if self.validate_path(input_path):
            self.curr_path = os.path.expanduser(input_path)
            self.idx = 0  # Reset cursor to the top of the new directory
            self.scroll_pos = 0
            self.update_files()
        else:
            self.display_error("Invalid path! Returning to navigation.")

    def navigate(self):
        """
        Main loop for rendering the files TUI and handling of user input.

        Listens for input to update the TUI, quitting when `q` is received.
        """
        while True:
            if self.is_terminal_small():
                self.display_error('Terminal too small!!')
            self.render()
            key = self.stdscr.getch()
            _key_press(self.stdscr, key, self)
            if curses.isendwin():
                break
