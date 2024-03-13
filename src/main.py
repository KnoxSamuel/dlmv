#!/usr/bin/env python3
# src/main.py

import os
import curses as c
import argparse
from utils.file_navigator import FileNavigator
from utils.cloney import Cloney

def parse_args():
    """
    Parse command line arguments for the dlmv tool runtime.

    Returns:
        An argparse.Namespace object containing all the command line arguments.
    """
    prs = argparse.ArgumentParser(description='dlmv: a TUI download manager tool for quickly choosing \
                                                a destination path near the working directory.')
    prs.add_argument('--cloney', help='Clone a repository using git', action='store_true')
    prs.add_argument('repo_url', nargs='?', help='The URL of the repository to clone')
    prs.add_argument('--options', nargs='*', help='Additional options for git clone')
    return prs.parse_args()

def main(stdscr, args: argparse.Namespace) -> None:
    """
    Main function for the dlmv tool.

    Parameters:
        stdscr: The main window object provided by curses.
        args: Parsed command line arguments.
    """
    if args.cloney and args.repo_url:
        options = args.options if args.options else []
        cloney_instance = Cloney(args.repo_url, options)
    else:
        cloney_instance = None

    c.curs_set(0) # hide cursor
    if c.has_colors():
        c.start_color()
        c.init_pair(1, c.COLOR_CYAN, c.COLOR_BLACK)  # For directories
        c.init_pair(2, c.COLOR_WHITE, c.COLOR_BLACK)  # For files

    file_navigator = FileNavigator(stdscr, cloney_instance)
    file_navigator.navigate()

if __name__ == "__main__":
    args = parse_args()
    c.wrapper(main, args)
