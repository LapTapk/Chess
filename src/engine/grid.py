from .vector2 import Vector2


def find_closest(grid, point):
    pts = grid.get_points()
    res = Vector2(0, 0)

    for i in range(len(pts)):
        for j in range(len(pts[0])):
            new_point = pts[i][j]
            cur_point = pts[res.x][res.y]
            cur = cur_point - point
            new = new_point - point
            if cur.length() > new.length():
                res = Vector2(i, j)

    return res


class Grid:
    def init(self, go, size, capacity):
        self.go = go

        check_size = size.x >= 0 and size.y >= 0
        if not check_size:
            raise ValueError

        self.size = size
        self.capacity = capacity

    def update(self):
        pass

    def get_points(self):
        size = self.size
        cap = self.capacity
        pos = self.go.position

        distX = size.x / cap.x
        distY = size.y / cap.y

        points = [[0] * cap.y for _ in range(cap.x)]
        for i in range(cap.x):
            for j in range(cap.y):
                offset = Vector2(i * distX, j * distY)
                points[i][j] = pos + offset

        return points


class GridBinder:
    def init(self, go, grd, coord, instant_bind=True):
        self.grd = grd
        self.coord = coord
        self.go = go
        self.binded = instant_bind

    def update(self):
        if not self.binded:
            return

        self.__bind()

    def __bind(self):
        points = self.grd.get_points()
        x, y = self.coord.to_tuple()

        self.go.position = points[x][y]
