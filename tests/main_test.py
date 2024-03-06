import pytest
from src.main import parse_args, main
from src.utils.file_navigator import FileNavigator
from src.commands.cloney import Cloney

def test_parse_args(mocker):
    mock_args = mocker.patch('argparse.ArgumentParser.parse_args', return_value=mocker.Mock(cloney=True, repo_url='https://github.com/user/repo.git', options=['--depth', '1']))
    args = parse_args()
    assert args.cloney
    assert args.repo_url == 'https://github.com/user/repo.git'
    assert args.options == ['--depth', '1']

def test_main(mocker):
    mock_args = mocker.Mock(cloney=True, repo_url='https://github.com/user/repo.git', options=['--depth', '1'])
    mock_cloney = mocker.patch('main.Cloney', return_value=mocker.Mock())
    mock_file_navigator = mocker.patch('main.FileNavigator', return_value=mocker.Mock())
    mock_curses_wrapper = mocker.patch('curses.wrapper')
    main(None, mock_args)
    mock_cloney.assert_called_once_with('https://github.com/user/repo.git', ['--depth', '1'])
    mock_file_navigator.assert_called_once_with(None, mock_cloney.return_value)
    mock_file_navigator.return_value.navigate.assert_called_once()
    