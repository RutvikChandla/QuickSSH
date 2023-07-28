import curses
import subprocess
import yaml
import os


MENU = ['Home', 'Play', 'Scoreboard', 'Exit']
FILTERED_MENU = MENU.copy()

def ssh_command(row):
    ip = row["ip"]
    return f'ssh -J user@hop user@{ip}'

def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    global MENU
    MENU = data
    global FILTERED_MENU
    FILTERED_MENU = MENU.copy()
    return data

def run_applescript(script):
    subprocess.run(['osascript', '-e', script])

def ssh_new_tab(item):
    
    if os.environ.get('TERM_PROGRAM') == 'iTerm.app':
      applescript_create_tab = 'tell application "iTerm" to tell current window to create tab with default profile'
      applescript_write_text = f'tell application "iTerm" to tell current session of current tab of current window to write text "{item}"'
      run_applescript(applescript_create_tab)
      run_applescript(applescript_write_text)
    else:
      #  same for terminal - not working
      applescript_create_tab = "osascript -e 'tell application \"Terminal\" to activate' \
      -e 'tell application \"System Events\" to keystroke \"t\" using {command down}' \
      -e 'tell application \"Terminal\" to do script \"echo hello\" in front window'"
      run_applescript(applescript_create_tab)
       

def print_menu(stdscr, selected_row_idx, search_input):
    stdscr.erase()
    # Print the search input in the top left corner
    stdscr.addstr(0, 0, "Search: " + search_input)
    # menu items should be filtered by the search input
    # substring, case insensitive
    global FILTERED_MENU
    FILTERED_MENU = [item for item in MENU if search_input.lower() in item["tag"].lower()]
    for idx, row in enumerate(FILTERED_MENU):
        print(row)
        y = idx + 2
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, 0, f'{idx} {row["tag"]} {row["nickname"]} {row["ip"]}')
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, 0, f'{idx} {row["tag"]} {row["nickname"]} {row["ip"]}')

    stdscr.refresh()

def main(stdscr):
    # Manual setup of the curses environment
    curses.curs_set(0)
    stdscr.keypad(1)
    curses.noecho()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # specify the current selected row
    current_row = 0

    # search input
    search_input = ""

    # print the menu
    print_menu(stdscr, current_row, search_input)

    while 1:
        key = stdscr.getch()
        stdscr.clear() 
        if key == curses.KEY_UP:
            if current_row > 0:
              current_row -= 1
            else:
              current_row = len(FILTERED_MENU)-1
        elif key == curses.KEY_DOWN:
            if current_row < len(FILTERED_MENU)-1:
              current_row += 1
            else:
              current_row = 0
        elif key == curses.KEY_ENTER or key in [10, 13]:
            ssh_new_tab(ssh_command(FILTERED_MENU[current_row]))
        elif key == curses.KEY_BACKSPACE or key == 127:
            # handle backspace/delete
            search_input = search_input[:-1]
        else:
            if chr(key).isalnum():
                search_input += chr(key)
                current_row = 0
        print_menu(stdscr, current_row, search_input)

    # Manual teardown of the curses environment
    curses.curs_set(1)
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
  yaml_file_path = '<path to conf.yaml>'
  res = read_yaml_file(yaml_file_path)
  curses.wrapper(main)

