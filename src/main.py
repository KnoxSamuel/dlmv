#!/usr/bin/env python3
# src/main.py

import os
import curses
from utils.file_navigator import FileNavigator
import argparse
from commands.cloney import Cloney

def parse_args():
    prs = argparse.ArgumentParser(description='dlmv TUI/CLI tool')
    prs.add_argument('--cloney', help='Clone a repository using git', action='store_true')
    prs.add_argument('repo_url', nargs='?', help='The URL of the repository to clone')
    prs.add_argument('--options', nargs='*', help='Additional options for git clone')
    return prs.parse_args()

def main(stdscr, args):
    cloney_instance = None
    if args.cloney and args.repo_url:
        options = args.options if args.options else []
        cloney_instance = Cloney(args.repo_url, options)
        #cloney_instance.clone()

    # Initialize curses interface if not cloning
    #s = curses.initscr()
    curses.curs_set(0)
    #sh, sw = s.getmaxyx()

    file_navigator = FileNavigator(stdscr, cloney_instance)
    file_navigator.navigate()

if __name__ == "__main__":
    args = parse_args()
    curses.wrapper(main, args)
