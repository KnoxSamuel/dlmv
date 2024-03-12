from setuptools import setup, find_packages

setup(
    name='dlmv',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dlmv=src.main:main',
        ],
    },
    install_requires=[
        # package dependencies
        'pytest',
        'windows-curses; platform_system=="Windows"'
    ],
    python_requires='>=3.6',
)
