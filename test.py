import os
import subprocess

def run_applescript(script):
    subprocess.run(['osascript', '-e', script])

def is_running_in_iterm():
    return os.environ.get('TERM_PROGRAM') == 'iTerm.app'

def iterm(item):
    if is_running_in_iterm():
        applescript_create_tab = 'tell application "iTerm" to tell current window to create tab with default profile'
        applescript_write_text = f'tell application "iTerm" to tell current session of current tab of current window to write text "{item}"'

        run_applescript(applescript_create_tab)
        run_applescript(applescript_write_text)
    else:
        print(f"Running in Terminal, executing command: {item}")
        # Add your code to handle Terminal behavior here

if __name__ == "__main__":
    # Example usage:
    iterm("echo 'Hello from Python'")
