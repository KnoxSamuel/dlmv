# src/commands/cloney.py

import subprocess
import sys
import curses
import os

class Cloney:
    def __init__(self, repo_url: str, options: list = None) -> None:
        self.repo_url = repo_url
        self.options = options if options else []

    def clone(self) -> None:
        command = ["git", "clone"] + self.options + [self.repo_url]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing git clone: {e}", file=sys.stderr)

'''
TODO: - [ ] Wrap git clone in class Cloney to pass options to git-clone(1)
            like so: 
                `dlmv cloney [--options] <args> <repo_url>`

      - [ ] Integration with dlmv: Ensure that the Cloney class can be easily
            integrated with the rest of the dlmv tool, likely through a
            command-line argument that triggers the cloning feature.

[samuel@samuel-rpi (git-cloney) ~/src/dlmv$] python3 src/main.py
Traceback (most recent call last):
  File "/home/samuel/src/dlmv/src/main.py", line 32, in <module>
    curses.wrapper(main, args)
  File "/usr/lib/python3.10/curses/__init__.py", line 94, in wrapper
    return func(stdscr, *args, **kwds)
TypeError: main() takes 1 positional argument but 2 were given

'''
