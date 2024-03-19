# src/utils/commands/cloney.py

import subprocess
import sys
import os
from typing import Optional, List

class Cloney:
    """
    The Cloney class provides functionality to emulate `git clone`.

    Attributes:
        repo_url (str): The URL of the repository to clone.
        options (Optional[List[str]], optional): Additional `git clone` options.
        dest (str, optional): destination path for repo. Defaults to "".

    Methods:
        __init__(self, repo_url: str, 
                options: Optional[List[str]] = None, dest: str = ""): Initializes a Cloney object.
        clone(): Clone the repository specified by `self.repo_url` to the destination directory.
    """
    
    def __init__(self, repo_url: str, options: Optional[List[str]] = None, dest: str = "") -> None:
        """
        Initializes a Cloney object.

        """
        self.repo_url = repo_url
        self.options = options if options else []
        self.dest = dest

    def clone(self) -> None:
        """
        Clone the repository specified by `self.repo_url` to the destination directory.

        If `self.dest` is provided, the repository will be cloned to the specified destination directory.
        Otherwise, the repository will be cloned to a directory with the same name as the repository.

        Raises:
            subprocess.CalledProcessError: If an error occurs while executing the `git clone` command.
        """
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
