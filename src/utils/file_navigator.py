# src/utils/file_navigator.py

import curses
import os
from commands.cloney import Cloney

class FileNavigator:
    def __init__(self, stdscr, cloney_instance=None):
        self.stdscr = stdscr
        self.cloney_instance = cloney_instance
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
        
    def validate_path(path):
        return os.path.exists(path) and os.path.isdir(path)
    
    def prompt_custom_path(self):
        # switch to echo mode to allow path entry
        curses.echo()
        self.stdscr.addstr(self.height - 1, 1, "Enter custom path: ")
        self.stdscr.refresh()
        custom_path = self.stdscr.getstr(self.height - 1, 20, 60).decode('utf-8')
        curses.noecho() # turn echo off after entry
        
        if self.validate_path(custom_path):
            self.current_path = custom_path
            self.refresh_files()
            self.selected_index = 0
        else:
            self.display_error("Invalid path.")

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
            elif key == ord('c') and self.cloney_instance:
                self.stdscr.addstr(self.height - 1, 1, "Cloning... Please wait.", curses.A_REVERSE)
                self.stdscr.refresh()
                self.cloney_instance.dest = self.current_path
                self.cloney_instance.clone()
                self.stdscr.addstr(self.height - 1, 1, "Cloning complete. Press any key to continue...", curses.A_REVERSE)
                self.stdscr.getch()
            elif key == ord('p'):
                self.prompt_custom_path()
