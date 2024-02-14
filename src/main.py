import curses
import os
from utils.file_navigator import FileNavigator

def main(stdscr):
    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()

    file_navigator = FileNavigator(stdscr)
    file_navigator.navigate()

if __name__ == "__main__":
    curses.wrapper(main)
