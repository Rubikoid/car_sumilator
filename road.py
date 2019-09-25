import curses
from rect import Rectangle


class Road(object):
    cur = None

    def __init__(self, x, y, rlen, rzone, up=False, name="r"):
        if x < 1 or y < 1:
            raise Exception("Can't place road")
        self.xPos, self.yPos = x, y
        self.rLen, self.rZone = rlen, rzone
        self.up = up
        self.xPos2 = self.xPos + (self.rZone if self.up else self.rLen)
        self.yPos2 = self.yPos + (self.rZone if not self.up else self.rLen)
        self.name = name
        self.connectors = []

    def roadIter(self):
        # if self.up:
        dX = 0
        dY = 0
        if self.up:
            for y in range(self.yPos, self.yPos2):
                yield ((self.xPos - 1, y), 1)
                yield ((self.xPos2, y), 1)
        else:
            for x in range(self.xPos, self.xPos2):
                yield ((x, self.yPos - 1), 1)
                yield ((x, self.yPos2), 1)
            # dX = 1
            # else:
            #    dY = 1
        for y in range(self.yPos - dY, self.yPos2 + dY):
            for x in range(self.xPos - dX, self.xPos2 + dX):
                # if (y == self.yPos - dY or self.yPos2 + dY) and dY != 0:
                #    yield ((x, y), 1)
                # if (x == self.xPos - dX or x == self.xPos2 + dX) and dX != 0:
                #    yield ((x, y), 1)
                # else:
                yield ((x, y), 0)

    def update(self, init=False):
        if not init:
            return
        roadChar = '|' if self.up else "-"  # "|"
        bRoadChar = curses.ACS_VLINE if self.up else curses.ACS_HLINE
        for k in self.roadIter():
            i, e = k
            x, y = i
            if e == 0:
                self.cur.addch(x, y, roadChar)
            elif e == 1:
                borderCheck = True
                for j in self.connectors:
                    if i in j.getRoad(self).getRect():
                        borderCheck = False
                        break
                if borderCheck:
                    self.cur.addch(x, y, bRoadChar)
        """
        if self.up:
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
        """

    def onRoad(self, x, y):
        return (self.xPos <= x and x < self.xPos2) and (self.yPos <= y and y < self.yPos2)

    def getRect(self):  # basic rect
        return Rectangle(self.xPos, self.yPos, self.xPos2, self.yPos2)

    def getConnectorRect(self):  # extended road rectangle
        return Rectangle(self.xPos + (0 if self.up else -1), self.yPos + (-1 if self.up else 0), self.xPos2 + (0 if self.up else +1), self.yPos2 + (+1 if self.up else 0))

    def __repr__(self):
        return f"Road {self.name}"


"""
    

    def getRealRect(self):
        return Rectangle(self.x, self.y, self.x + self.w, self.y + self.h)

    def xmin(self):
        return self.x if self.up else (self.x - 2)

    def xmax(self):
        return self.x + self.w if self.up else (self.x + self.w + 1)

    def ymin(self):
        return (self.y) if not self.up else (self.y - 1)

    def ymax(self):
        return (self.y + self.h) if not self.up else (self.y + self.h + 1)
"""


class SimpleConnector(object):
    def __init__(self, r0, r1):
        self.r0 = r0
        self.r1 = r1
        self.e = self.r0.getConnectorRect() & self.r1.getConnectorRect()
        if self.e is not None:
            r0.connectors.append(self)
            r1.connectors.append(self)
        else:
            raise Exception(
                f"No intersect\n{self.r0.getConnectorRect()} {self.r0.getConnectorRect()}\n{self.r1.getConnectorRect()} {self.r1.getConnectorRect()}\n{self.e}")

    def getRoad(self, road):
        return self.r0 if road == self.r1 else self.r1
