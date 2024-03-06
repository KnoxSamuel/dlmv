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
        self.scroll_pos = 0

    def refresh_files(self):
        self.files = os.listdir(self.current_path)

    def draw(self):
        if self.height < 4 or self.width < 20:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Terminal too small.", curses.A_REVERSE)
            self.stdscr.refresh()
            return

        self.stdscr.clear()
        self.window.clear()
        self.stdscr.box()

        # Display the current path above border
        self.stdscr.addstr(0, 1, f" Current Path: {self.current_path} ", curses.A_REVERSE)

        visible_files = self.files[self.scroll_pos:self.scroll_pos + self.height - 4]

        for i, file in enumerate(visible_files):
            if self.selected_index == self.scroll_pos + i:
                self.window.addstr(i+1, 1, file, curses.A_REVERSE)
            else:
                self.window.addstr(i+1, 1, file)

        self.stdscr.refresh()
        self.window.refresh()

    def display_error(self, message):
        y, x = self.stdscr.getyx()
    
        self.stdscr.move(self.height - 2, 1)
        self.stdscr.clrtoeol()
        self.stdscr.addstr(message, curses.A_REVERSE)
        self.stdscr.refresh()
        curses.napms(2000)  # pause for 2 seconds
    
        # clear the error message after displaying it
        self.stdscr.move(self.height - 2, 1)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()
    
        # restore cursor position
        self.stdscr.move(y, x)

    def validate_path(self, path):
        expanded_path = os.path.expanduser(path)
        return os.path.exists(expanded_path) and os.path.isdir(expanded_path)
    
    def prompt_custom_path(self):
        # switch to echo mode to allow path entry
        curses.echo()
        self.stdscr.addstr(self.height - 1, 1, "Enter custom path: ")
        self.stdscr.refresh()
        custom_path = self.stdscr.getstr(self.height - 1, 20, 60).decode('utf-8')
        curses.noecho() # turn echo off after entry

        expanded_path = os.path.expanduser(custom_path)

        if self.validate_path(expanded_path):
            self.current_path = expanded_path
            self.refresh_files()
            self.selected_index = 0
        else:
            self.display_error("Invalid path.")

    def navigate(self):
        while True:
            self.draw()
            key = self.stdscr.getch()

            max_scroll = max(0, len(self.files) - (self.height - 4))
            max_index = len(self.files) - 1

            if key in [curses.KEY_UP, ord('k')]:
                if self.selected_index > 0:
                    self.selected_index -= 1
                if self.selected_index < self.scroll_pos:
                    self.scroll_pos = max(0, self.scroll_pos - 1)
            
            elif key in [curses.KEY_DOWN, ord('j')]:
                if self.selected_index < max_index:
                    self.selected_index += 1
                if self.selected_index >= self.scroll_pos + self.height - 4:
                    self.scroll_pos = min(max_scroll, self.scroll_pos + 1)
            
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
                curses.endwin()
                break
            
            elif key == ord('c') and self.cloney_instance:
                self.stdscr.addstr(self.height - 1, 1, "Cloning... Please wait.", curses.A_REVERSE)
                self.stdscr.refresh()
                self.cloney_instance.dest = self.current_path
                self.cloney_instance.clone()
                self.stdscr.addstr(self.height - 1, 1, "Cloning complete. Press any key to continue...", curses.A_REVERSE)
                self.stdscr.getch()
                self.refresh_files()
            
            elif key == ord('p'):
                self.prompt_custom_path()
            
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.stdscr.getmaxyx()
                self.window.resize(self.height - 2, self.width - 2)
                if self.height < 4 or self.width < 20:
                    continue


