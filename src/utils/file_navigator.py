# src/utils/file_navigator.py

import curses
import os

class FileNavigator:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_path = os.getcwd()
        self.selected_index = 0
        self.refresh_files()
        self.height, self.width = stdscr.getmaxyx()
        self.window = curses.newwin(self.height - 2, self.width - 2, 1, 1) # Window border

    def refresh_files(self):
        self.files = os.listdir(self.current_path)

    def draw(self):
        self.stdscr.clear()
        self.window.clear()
        self.stdscr.box()
        
        # Display the current path above border
        self.stdscr.addstr(0, 1, f" Current Path: {self.current_path} ", curses.A_REVERSE)

        for index, file in enumerate(self.files[:self.height - 4]):
            if index == self.selected_index:
                self.window.addstr(index + 1, 1, file, curses.A_REVERSE)
            else:
                self.window.addstr(index + 1, 1, file)
        
        self.stdscr.refresh()
        self.window.refresh()

    def navigate(self):
        while True:
            self.draw()
            key = self.stdscr.getch()

            if key in [curses.KEY_UP, ord('k')]:
                self.selected_index = max(0, self.selected_index - 1)
            elif key in [curses.KEY_DOWN, ord('j')]:
                self.selected_index = min(len(self.files) - 1, self.selected_index + 1)
            elif key in [curses.KEY_RIGHT, ord('l'), curses.KEY_ENTER, 10]:
                selected_file = self.files[self.selected_index]
                new_path = os.path.join(self.current_path, selected_file)
                if os.path.isdir(new_path):
                    self.current_path = new_path
                    self.refresh_files()
                    self.selected_index = 0
            elif key in [curses.KEY_LEFT, ord('h')]:
                if self.current_path != '/':
                    self.current_path = os.path.dirname(self.current_path)
                    self.refresh_files()
                    self.selected_index = 0
            elif key == ord('q'):
                break
