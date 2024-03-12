# dlmv, cli download manager

dlmv is a TUI download manager for quickly choosing a destination
path near the working directory.

## Installation

Download the source code.

``` sh
git clone {repo_url}
cd {repo_url}
```

Run `setup.py` install script with:

``` sh
pip install -r requirements.txt
pip install .
```

Now `dlmv` will activate the tool from anywhere on the filesystem.

## Usage

navigation tips:

``` md
('h / ←',           "exit folder (cd ..)"),
('l / → / enter',   "open folder (cd dir/)"),
('k/j / ↑/↓',       "scroll up/down"),
('c',               "clone"),
('p',               "custom path"),
('q',               "quit")
```

options: `dlmv --help`

``` sh
dlmv: a TUI download manager tool for quickly choosing a destination path near the working directory.

dlmv [OPTIONS]

--cloney: Clone a repository using git.
    repo_url: URL of the repository to clone.
--help: View help and additional options.
```

``` md
[ ] 2-3 quick start examples
```

## Contributing

Contributions are most welcome! Please follow these guidelines:

1. Fork the repository and create a new branch.
2. Push proposed changes to your fork.
3. Submit a pull request.

Or add a thread to the [GitHub issues tracker](https://github.com/KnoxSamuel/dlmv/issues).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Contact

If you have any questions or suggestions regarding this project, feel free to contact me at [knoxsa@oregonstate.edu](mailto:knoxsa@oregonstate.edu).
