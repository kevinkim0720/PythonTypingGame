# Words per minute test written in python- helped by Tech with Tim Youtuber

import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the Words Per Minute Test")
    stdscr.addstr("\nPress any key to begin")
    stdscr.refresh()
    # doesn't immediately close the program
    stdscr.getkey()

# =0 is a variable you don't need
def display_text(stdscr, target, current, wpm = 0):
    stdscr.addstr(target)
    stdscr.addstr(5,0, f"WPM: {wpm}")
    
    # gives index and char in an array, allows for overlaying text
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        try:
            stdscr.addstr(0, i, char, color)
        except curses.error:
            pass

def load_text():
    # context manager - closes after it's done
    with open("C:/Users/kevki/Documents/Python/TypingGame/text.txt", "r") as f:
        lines = f.readlines()
        # .strip() removes the leading or trailing whitespace characters
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    stdscr.clear()
    stdscr.addstr(target_text)
    stdscr.refresh()

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        # characters per minute divded by 5
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        # without clear method, the text will keep writing onto itself
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # combines every character in list into a string using the delimiter (separator)
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # need try and except because of the nodelay line
        try:
            key = stdscr.getkey()
        except:
            continue

        # esc key value in ASCII
        if ord(key) == 27:
            break
        
        # different ways to call backspace key
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)



# standard output (stdscr) - write stuff out to
def main(stdscr):
    # text color and background color
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(6,0, "Congratulation, you completed the test! \nPress any key to play again or esc to quit")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)