# src/commands/cloney.py

import subprocess
import sys
import curses
import os
from typing import Optional, List

class Cloney:
    def __init__(self, repo_url: str, options: Optional[List[str]] = None, dest: str = "") -> None:
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
