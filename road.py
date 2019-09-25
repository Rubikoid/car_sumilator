import curses
from rect import Rectangle


class Road(object):
    cur = None
    connectors = []

    def __init__1(self, x, y, w, h):
        if h == w:
            raise Exception("no square roads")
        # w > h - its not up
        # h > w - its up
        self.x, self.y, self.h, self.w = x, y, (h if h > w else (h + 1)), ((w + 1) if h > w else w)
        rlen = (h if h > w else w)
        rzone = (w if h > w else h)

    def __init__(self, x, y, rlen, rzone, up=False):
        self.x, self.y = x, y
        self.rlen, rzone = rlen, rzone

    def update(self, init=False):
        if not init:
            return

        if self.up():
            for y in range(self.y, self.y + self.h):
                # PIECE OF SHIT CODE
                allowdL, allowdR = True, True
                for i in self.connectors:
                    if (self.x, y) in i.e:
                        allowdL = False
                    if (self.x+self.w, y) in i.e:
                        allowdR = False
                if allowdL:
                    self.cur.addch(self.x, y, curses.ACS_VLINE)
                if allowdR:
                    self.cur.addch(self.x + self.w, y, curses.ACS_VLINE)
                for x in range(self.x + 1, self.x + self.w):
                    self.cur.addch(x, y, "_")
        else:
            for x in range(self.x, self.x + self.w):
                # PIECE OF SHIT CODE
                allowdU, allowdD = True, True
                for i in self.connectors:
                    if (x, self.y) in i.e:
                        allowdU = False
                    if (x, self.y+self.h) in i.e:
                        allowdD = False
                if allowdU:
                    self.cur.addch(x, self.y, curses.ACS_HLINE)
                if allowdD:
                    self.cur.addch(x, self.y + self.h, curses.ACS_HLINE)
                for y in range(self.y + 1, self.y + self.h):
                    self.cur.addch(x, y, "|")

    def up(self):
        return self.h > self.w

    def onRoad(self, x, y):
        return (self.x <= x and x < self.x + self.w) and (self.y < y and y < self.y + self.h)

    def getRect(self):
        return Rectangle(self.xmin(), self.ymin(), self.xmax(), self.ymax())

    def getRealRect(self):
        return Rectangle(self.x, self.y, self.x + self.w, self.y + self.h)

    def xmin(self):
        return self.x if self.up() else (self.x - 2)

    def xmax(self):
        return self.x + self.w if self.up() else (self.x + self.w + 1)

    def ymin(self):
        return (self.y) if not self.up() else (self.y - 1)

    def ymax(self):
        return (self.y + self.h) if not self.up() else (self.y + self.h + 1)


class SimpleConnector(object):
    def __init__(self, r0, r1):
        self.r0 = r0
        self.r1 = r1
        self.e = self.r0.getRect() & self.r1.getRect()
        if self.e is not None:
            r0.connectors.append(self)
            r1.connectors.append(self)
        else:
            raise Exception(f"No intersect\n{self.r0.getRect()} {self.r0.getRealRect()}\n{self.r1.getRect()} {self.r1.getRealRect()}\n{self.e}")

    def getRoad(self, road):
        return self.r0 if road == self.r1 else self.r1
