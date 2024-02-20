# src/commands/cloney.py

import subprocess
import sys
import curses
import os

class Cloney:
    def __init__(self, repo_url: str, options: list=None, dest: str=None) -> None:
        self.repo_url = repo_url
        self.options = options if options else []
        self.dest = dest

    def clone(self) -> None:
        command = ["git", "clone"] + self.options + [self.repo_url]
        if self.dest:
            command.append(self.dest)
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing git clone: {e}", file=sys.stderr)

'''
TODO: - [ ] Wrap git clone in class Cloney to pass options to git-clone(1)
            like so: 
                `dlmv --cloney <repo_url>`

      - [ ] Integration with dlmv: Ensure that the Cloney class can be easily
            integrated with the rest of the dlmv tool, likely through a
            command-line argument that triggers the cloning feature.

'''
