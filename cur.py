import curses
import traceback
import itertools
import road


class ObjMap(object):
    m = []

    def __init__(self, x, y):
        self.m = [[' ' for _ in range(x)] for _ in range(y)]

    def setCH(self, x, y, c):
        self.m[y][x] = c

    def getCH(self, x, y):
        return self.m[y][x]


class Cur(object):
    _class_update_list = []
    objs = []

    def __init__(self):
        self.objs = []

    def init(self):
        self.stdscr = curses.initscr()
        if not self.stdscr:
            print("Unable to init curses")
            exit(1)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        self.stdscr.keypad(True)

    def do(self, func, efunc):
        e = ""
        try:
            for i in Cur._class_update_list:
                i.cur = self
            func(self)
        except Exception as ex:
            e = traceback.format_exc()
        finally:
            for i in Cur._class_update_list:
                i.cur = None
            efunc(self)
        print(e)

    def makekek(self):
        self.pad = curses.newpad(100, 100)
        self.omap = ObjMap(100, 100)

        for i in itertools.combinations([i for i in self.objs if isinstance(i, road.Road)], 2):
            f = i[0].getRect() & i[1].getRect()
            if f is not None:
                raise Exception(f"Road collision found!\n{i[0].getRect()}\n{i[1].getRect()}")

        for i in self.objs:
            i.update(init=True)

        _fps = 0
        while True:
            self.pad.refresh(0, 0, 0, 0, 40, 100)
            _fps = (_fps + 1) % 20
            if _fps == 0:
                for i in self.objs:
                    i.update()
            curses.napms(10)

    def addch(self, x, y, ch):
        self.pad.addch(y, x, ch)
        self.omap.setCH(x, y, ch)

    def getch(self, x, y):
        return self.omap.getCH(x, y)

    def stop(self):
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(False)
        curses.curs_set(True)
        curses.endwin()
        print("Finish")
        # print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in a.omap.m]))
