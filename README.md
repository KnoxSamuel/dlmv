# dlmv, cli download manager

`dlmv` is a TUI download manager for quickly choosing a destination
path near the working directory, or simple filesystem navigation.

## Prerequisites

Before you can install `dlmv`, make sure you have the following prerequisites installed:

- Python (3.8+): Download and install from [python.org](https://www.python.org/downloads/) or use your operating system's package manager.
- pip: Usually comes with Python. If not, follow the [installation instructions](https://pip.pypa.io/en/stable/installation/).
- git: Download and install from [git-scm.com](https://git-scm.com/downloads).

## Installation

Download the source code.

``` sh
git clone https://github.com/KnoxSamuel/dlmv.git
cd dlmv
```

Install required dependencies.

``` sh
pip install -r requirements.txt
```

Install the `dlmv` package.

``` sh
pip install .
```

After installation, `dlmv` can be activated from anywhere on the filesystem.

## Usage

Basic usage to open the TUI for filesystem navigation

``` sh
dlmv

# if setuptools is giving you issues:
cd dlmv/
python3 src/dlmv/main.py
python3 src/dlmv/main.py --cloney <repo_url>
```

Clone a repository using the --cloney option

``` sh
dlmv --cloney https://github.com/<username>/<repo_url>.git
```

Display help options

``` sh
dlmv --help
```

Navigation:

``` sh
('h / ←',           "exit folder (cd ..)"),
('l / → / enter',   "open folder (cd dir/)"),
('k/j / ↑/↓',       "scroll up/down"),
('c',               "clone here"),
('p',               "custom path"),
('q',               "quit")
```

## Development Environment

Follow these steps to set up a development environment for dlmv.

Create a virtual environment.

``` sh
python -m venv venv
```

Activate the virtual environment.

``` sh
On Windows:
.\venv\Scripts\activate

On Unix or MacOS:
source venv/bin/activate
```

Install required dependencies.

``` sh
pip install -r requirements.txt
```

Once the dev environment is set up, you can make changes to the codebase. Test your changes with:

``` sh
python -m unittest discover tests
```

Build the executable by running:

``` sh
python setup.py install
```

Ensure that the executable created can be invoked from the command line using the dlmv command.

For any issues during installation or setting up the development environment, check the [GitHub issues tracker](https://github.com/KnoxSamuel/dlmv/issues) for similar problems or to add a new issue.

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
