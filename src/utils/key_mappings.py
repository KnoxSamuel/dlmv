# src/utils/key_mappings.py

import curses as c
import os

def _key_press(key, nav):
    """
    Handle user key presses by mapping them to file navigator actions.
    
    Parameters:
        key: The key pressed by the user.
        nav: The FileNavigator instance.
    """
    max_scroll = max(0, len(nav.files) - (nav.h - 4))

    key_actions = {
        ord('h'):           lambda: nav_back(nav),
        c.KEY_LEFT:         lambda: nav_back(nav),
        ord('j'):           lambda: move_down(nav, max_scroll),
        c.KEY_DOWN:         lambda: move_down(nav, max_scroll),
        ord('k'):           lambda: move_up(nav),
        c.KEY_UP:           lambda: move_up(nav),
        ord('l'):           lambda: nav_into(nav),
        c.KEY_RIGHT:        lambda: nav_into(nav),
        c.KEY_ENTER:        lambda: nav_into(nav),
        10:                 lambda: nav_into(nav),
        
        ord('c'):           lambda: clone_repo(nav) if nav.cloney_is else None,
        ord('p'):           lambda: nav.prompt_custom_path(),
        
        ord('q'):           lambda: _exit(),
        c.KEY_RESIZE:       lambda: resize_window(nav),
    }

    action = key_actions.get(key)
    action() if action else None

def move_up(nav):
    """
    Move the selection up in the file list.
    
    """
    if nav.idx > 0:
        nav.idx -= 1
    if nav.idx < nav.scroll_pos:
        nav.scroll_pos = max(0, nav.scroll_pos - 1)

def move_down(nav, max_scroll):
    """
    Move the selection down in the file list.
    
    """
    if nav.idx < len(nav.files) - 1:
        nav.idx += 1
    if nav.idx >= nav.scroll_pos + nav.h - 4:
        nav.scroll_pos = min(max_scroll, nav.scroll_pos + 1)

def nav_into(nav):
    """
    Navigate into the selected directory.
    
    """
    selected_file = nav.files[nav.idx]
    new_path = os.path.join(nav.curr_path, selected_file)
    if os.path.isdir(new_path):
        nav.curr_path = new_path
        nav.update_files()
        nav.idx = 0

def nav_back(nav):
    """
    Navigate back to the parent directory.
    
    """
    if nav.curr_path != '/':
        nav.curr_path = os.path.dirname(nav.curr_path)
        nav.update_files()
        nav.idx = 0

def _exit():
    """Exit the file nav."""
    c.endwin()

def clone_repo(nav):
    """
    Initiate the cloning process for the selected repository.
    
    """
    nav.stdscr.addstr(nav.h - 1, 1, "Cloning... Please wait.", c.A_REVERSE)
    nav.stdscr.refresh()
    nav.cloney_is.dest = nav.curr_path
    nav.cloney_is.clone()
    nav.stdscr.addstr(nav.h - 1, 1, "Cloning complete. Press any key to continue...", c.A_REVERSE)
    nav.stdscr.getch()
    nav.update_files()

def resize_window(nav):
    """
    Handle terminal window resize events.

    """
    nav.h, nav.w = nav.stdscr.getmaxyx()
    nav.window.resize(nav.h - 2, nav.w - 2)
    if nav.h < 4 or nav.w < 20:
        return  # Do nothing if window is too small
    