from setuptools import setup, find_packages

setup(
    name='dlmv',
    version='0.1.1',
    author='Samuel Knox',
    author_email='knoxsa@oregonstate.edu',
    description='dlmv is a TUI download manager for quickly choosing a destination path near the working directory.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_dir={'dlmv': 'src/dlmv'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'dlmv=dlmv.main:main',
        ],
    },
    install_requires=[
        # package dependencies
        'pytest',
        'windows-curses; platform_system=="Windows"'
    ],
    python_requires='>=3.8',
)
