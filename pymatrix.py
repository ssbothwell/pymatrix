#!/usr/bin/env python
import curses, math, time
from random import randint

class window:
    def __init__(self, x, y):
        self.rows = screen.getmaxyx()[0]-1
        self.cols = screen.getmaxyx()[1]-4
        self.win = screen# curses.newwin(self.rows, self.cols, 1, 2)
        self.vert_strings = []
        self.singletons = []
        # Add a border to the window
        self.win.border(0)
        for _ in range(0, math.floor(self.cols/2)):
            # create a vertical string
            self.create_vert_string()
            # refresh window and wait for user input
        for _ in range(0, self.cols//2):
            self.create_singleton_char()
        self.win.refresh()

    def create_vert_string(self):
        new_string = vertical_string(self.win)
        self.vert_strings.append(new_string)
        new_string.write()

    def create_singleton_char(self):
        x = randint(1, self.cols-2)
        y = randint(1, self.rows-2)
        new_singleton = singleton_char(y, x, self.win)
        self.singletons.append(new_singleton)

    def animate(self):
        Q = -1
        while Q != ord('q'):
            self.controls(Q)
            for vert_string in self.vert_strings:
                vert_string.move()
            self.create_singleton_char()
            self.refresh()
            Q = screen.getch()
            time.sleep(0.1)

    def del_vert_string(self, key):
        vert_string = self.vert_strings[key]
        vert_string.erase()
        self.vert_strings.remove(vert_string)
        self.refresh()

    def refresh(self):
        self.win.refresh()

    def getch(self):
        self.win.getch()

    def resize(self):
        self.win.clear()
        self.rows = screen.getmaxyx()[0]-1
        self.cols = screen.getmaxyx()[1]-1
        self.win.border(0)

    def controls(self, key):
            if key == curses.KEY_RESIZE:
                self.resize()
            elif key == ord('j') and len(self.vert_strings) > 0:
                # remove a vert string
                self.del_vert_string(-1)
            elif key == ord('J') and len(self.vert_strings) > 10:
                for _ in range(0,10):
                    self.del_vert_string(-1)
            elif key == ord('k'):
                # add a vert string
                self.create_vert_string()
            elif key == ord('K'):
                for _ in range(0,10):
                    self.create_vert_string()

class singleton_char:
    def __init__(self, y, x, window):
        self.char = chr(randint(32,126))
        self.x = x
        self.y = y
        self.window = window
        self.write()

    def write(self):
        if randint(0,1) == 1:
            self.window.addch(self.y, self.x, self.char, curses.A_BOLD)
        else:
            self.window.addch(self.y, self.x, self.char, curses.A_DIM)

    def erase(self):
        self.window.addch(self.y, self.x, ' ')


class vertical_string:
    def __init__(self, window):
        self.length = randint(6,15)
        self.chars = [ chr(randint(32, 126)) for _ in range(0, self.length) ]
        self.window = window
        self.x = randint(1, self.window.getmaxyx()[1]-1)
        self.y = randint(1, self.window.getmaxyx()[0]-1)

    def write(self):
        if self.y < 1:
            visible_chars = -(self.length + self.y)
            for i, ch in enumerate(self.chars[visible_chars:]):
                if i < 3 or i >= self.length - 3:
                    self.window.addstr(i+1, self.x, ch)
                else:
                    self.window.addstr(i+1, self.x, ch, curses.A_BOLD)
        else:
            for i, ch in enumerate(self.chars):
                if i < 3 or i >= self.length - 3:
                    if self.y+i < self.window.getmaxyx()[0]-1:
                        self.window.addstr(self.y+i, self.x, ch)
                elif self.y+i < self.window.getmaxyx()[0]-1:
                    self.window.addstr(self.y+i, self.x, ch, curses.A_BOLD)

    def reset(self):
        self.length = randint(5,15)
        self.chars = [ chr(randint(32, 126)) for _ in range(0, self.length) ]

    def move(self):
        self.erase()
        if self.y+1 < self.window.getmaxyx()[0]-1:
            self.y += 1
            self.write()
        else:
            self.reset()
            self.y = 1 - self.length
            self.x =  randint(1, self.window.getmaxyx()[1]-2)

    def erase(self):
        if self.y < 1:
            visible_chars = -(self.length + self.y)
            for i, ch in enumerate(self.chars[visible_chars:]):
                self.window.addch(i+1, self.x, ' ')
        else:
            for i, ch in enumerate(self.chars):
                if self.y+i < self.window.getmaxyx()[0]-1:
                    self.window.addch(self.y+i, self.x, ' ')


if __name__ == '__main__':
    screen = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1);

    # no delay
    screen.nodelay(1)
    # Turn off key echoing
    curses.noecho()
    # respond to key presses imediately (no enter key)
    curses.cbreak()
    # Hide the cursor
    curses.curs_set(0)
    # create window object
    win = window(160, 24)
    win.animate()
    curses.endwin()
