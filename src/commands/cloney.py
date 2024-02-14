import subprocess
import sys
import curses
import os

class Cloney:
    def __init__(self, repository_url: str, options: list = None) -> None:
        self.repository_url = repository_url
        self.options = options if options else []
        
    def clone(self) -> None:
        command = ["git", "clone"] + self.options + [self.repository_url]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing git clone: e", file=sys.stderr)
    
    '''
    TODO: - [ ] Wrap git clone in class Cloney to pass options to git-clone(1)
                like so: `dlmv cloney --options <argument> <repository>`
        
        Integration with dlmv: Ensure that the Cloney class can be easily integrated with the rest of the dlmv tool, likely through a command-line argument that triggers the cloning feature.
    '''
