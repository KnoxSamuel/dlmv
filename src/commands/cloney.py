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
        repo_name = self.repo_url.split('/')[-1].split('.')[0] # parse project name for dest path
        if self.dest:
            final_dest = os.path.join(self.dest, repo_name)
        else:
            final_dest = repo_name
        
        command = ["git", "clone"] + self.options + [self.repo_url, final_dest]
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
