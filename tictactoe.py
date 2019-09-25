import curses
import traceback


class Cur(object):
    _x = 0
    _y = 0
    omap = None
    lc = 'X'

    def __init__(self):
        self.omap = [[-1 for _ in range(3)] for _ in range(3)]

    def init(self):
        self.stdscr = curses.initscr()
        if not self.stdscr:
            print("Unable to init curses")
            exit(1)

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def do(self, func, efunc):
        e = ""
        try:
            func(self)
        except Exception as ex:
            e = traceback.format_exc()
        finally:
            efunc(self)
        print(e)

    def makekek(self):
        self.pad = self.stdscr

        for y in range(0, 5):
            for x in range(0, 5):
                if x % 2 == 1:
                    if y % 2 == 1:
                        self.addch(x, y, curses.ACS_SSSS)
                    else:
                        self.addch(x, y, curses.ACS_VLINE)
                elif y % 2 == 1:
                    self.addch(x, y, curses.ACS_HLINE)

        self.pad.move(self._y, self._x)
        while True:
            e = self.pad.getch()
            if e == curses.KEY_LEFT:
                self._x = (self._x - 2) % 6
            elif e == curses.KEY_RIGHT:
                self._x = (self._x + 2) % 6
            elif e == curses.KEY_UP:
                self._y = (self._y - 2) % 6
            elif e == curses.KEY_DOWN:
                self._y = (self._y + 2) % 6
            elif e == ord('q'):
                break
            elif e == 32:
                if self.doMove():
                    e = self.pad.getch()
                    break
            self.pad.move(self._y, self._x)

    def check(self, c, e=0):
        for y in self.omap:
            if set(y) == set(c):
                return True
        for x in range(len(self.omap[0])):
            if set(y[x] for y in self.omap) == set(c):
                return True
        if set(self.omap[k][k] for k in range(len(self.omap))) == set(c):
            return True
        if set(self.omap[-k-1][k] for k in range(len(self.omap))) == set(c):
            return True
        self.pad.refresh()
        return False

    def doMove(self):
        if self.omap[self._y//2][self._x//2] == -1:
            self.addch(self._x, self._y, self.lc)
            self.omap[self._y//2][self._x//2] = (0 if self.lc == 'X' else 1)
            if self.check(((0 if self.lc == 'X' else 1),)):
                self.stdscr.clear()
                self.stdscr.addstr(0, 0, f"{self.lc} WIN")
                self.stdscr.refresh()
                return True
            self.lc = ('0' if self.lc == 'X' else 'X')
        return False

    def addch(self, x, y, ch):
        self.pad.addch(y, x, ch)

    def stop(self):
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(False)
        curses.endwin()
        print("Finish")


a = Cur()
a.init()
a.do(Cur.makekek, Cur.stop)
