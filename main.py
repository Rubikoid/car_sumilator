import road
import cur


class Dirs(object):
    _LEFT = 0
    _TOP = 1
    _RIGHT = 2
    _DOWN = 3

    def doDir(_DIR):
        return (_DIR + 1) % 4

    def __str__(_DIR):
        if _DIR == Dirs._LEFT:
            return "LEFT   "
        elif _DIR == Dirs._RIGHT:
            return "RIGHT  "
        elif _DIR == Dirs._TOP:
            return "UP     "
        elif _DIR == Dirs._DOWN:
            return "DOWN   "


class Car(object):
    x = 0
    y = 0
    _x = 0
    _y = 0
    cur = None

    _ch = '\0'

    def __init__(self, x, y):
        # self.x, _x = x, x
        # self.y, _y = y, y
        self.x = x
        self.y = y

    def isMove(self):
        return self._y != self.y or self._x != self.x

    def _update(self):
        self._x = self.x
        self._y = self.y

    def update(self, init=False):
        if init:
            return

        if self.isMove():
            if self._ch != '\0':
                self.cur.addch(self._x, self._y, self._ch)
                self.cur.pad.move(20, 20)
                self.cur.pad.addch(20, 20, self._ch)
            self._ch = self.cur.getch(self.x, self.y)
            self.cur.addch(self.x, self.y, '@')

        self._update()


class SimpleCar(Car):
    road = None
    roadChange = False
    direction = 2

    def __init__(self, x, y):
        super().__init__(x, y)

    def _doMove(self, dX, dY):
        _dX = 0
        _dY = 0
        if self.road.onRoad(self.x + dX, self.y+dY):
            _dX += dX
            _dY += dY
        else:
            for i in self.road.connectors:
                if i.getRoad(self.road).onRoad(self.x + dX, self.y+dY):
                    self.road = i.getRoad(self.road)
                    _dX += dX
                    _dY += dY
                    self.roadChange = True
                    break
        return _dX, _dY

    def _update(self):
        super()._update()
        dX = 0
        dY = 0
        if self.direction == Dirs._TOP:
            dtX, dtY = self._doMove(0, -1)
        elif self.direction == Dirs._DOWN:
            dtX, dtY = self._doMove(0, 1)
        elif self.direction == Dirs._RIGHT:
            dtX, dtY = self._doMove(1, 0)
        elif self.direction == Dirs._LEFT:
            dtX, dtY = self._doMove(-1, 0)
        else:
            dtX, dtY = 0, 0
        dX += dtX
        dY += dtY
        self.x += dX
        self.y += dY
        if self.roadChange:
            self.direction = Dirs.doDir(self.direction)
            self.roadChange = False

    def update(self, init=False):
        super().update()
        if init:
            return
        self.cur.pad.move(21, 20)
        self.cur.pad.addstr(21, 20, Dirs.__str__(self.direction))


cur._class_update_list = [Car, road.Road]

if __name__ == "__main__":
    a = cur.Cur()
    r0 = road.Road(1, 2, 15, 2, False, "r0")
    r1 = road.Road(r0.xPos2, r0.yPos-1, 9, 2, True, "r1")
    r2 = road.Road(r1.xPos - 8, r1.yPos2, 15, 2, False, "r2")
    r3 = road.Road(r2.xPos - 2, r0.yPos2, 12, 2, True, "r3")
    c0 = SimpleCar(4, 3)
    co0 = road.SimpleConnector(r0, r1)
    co1 = road.SimpleConnector(r1, r2)
    co2 = road.SimpleConnector(r0, r3)
    co3 = road.SimpleConnector(r2, r3)

    c0.road = r0
    c0.direction = Dirs._RIGHT
    a.objs.append(r0)
    a.objs.append(r1)
    a.objs.append(r2)
    a.objs.append(r3)
    a.objs.append(c0)

    a.init()
    a.do(cur.Cur.makekek, cur.Cur.stop)
    print(1337)
