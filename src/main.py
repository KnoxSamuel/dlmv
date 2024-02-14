import curses
import os
from utils.file_navigator import FileNavigator
import argparse
from commands.cloney import Cloney

def parse_args():
    prs = argparse.ArgumentParser(description='dlmv TUI/CLI tool')
    prs.add_argument('--clone', help='Clone a repository using git', action='store_true')
    prs.add_argument('repository_url', nargs='?', help='The URL of the repository to clone')
    prs.add_argument('--options', nargs='*', help='Additional options for git clone')
    return prs.parse_args()

def main(stdscr):
    if args.clone and args.repository_url:
        # git clone if --clone is specified
        options = args.options if args.options else []
        cloney_instance = Cloney(args.repository_url, options)
        cloney_instance.clone()
        return  # no curses tui?

    # Initialize curses interface if not cloning
    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()

    file_navigator = FileNavigator(stdscr)
    file_navigator.navigate()

if __name__ == "__main__":
    args = parse_args()
    curses.wrapper(main, args)
