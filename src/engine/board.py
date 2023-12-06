from vector2 import *
from grid import GridBinder


class Board:
    def init(self, go, figures):
        self.go = go
        self.figures = [[None] * 8 for _ in range(8)]
        for figure in figures:
            binder = figure.get_component(GridBinder)
            coord = binder.coord
            self.figures[coord.x][coord.y] = binder

    def update(self):
        pass

    def move(self, frm, to):
        figure = self.figures[frm.x][frm.y]

        figure.coord = to

        self.figures[frm.x][frm.y] = None
        self.figures[to.x][to.y] = figure


class Pawn:
    name = 'pawn'
    user_poses = (Vector2(i, 6) for i in range(8))
    enemy_poses = (Vector2(i, 1) for i in range(8))


class Rook:
    name = 'rook'
    user_poses = (from_tuple(i) for i in ((0, 7), (7, 7)))
    enemy_poses = (from_tuple(i) for i in ((0, 0), (7, 0)))


class Knight:
    name = 'knight'
    user_poses = (from_tuple(i) for i in ((2, 7), (5, 7)))
    enemy_poses = (from_tuple(i) for i in ((2, 0), (5, 0)))


class Bishop:
    name = 'bishop'
    user_poses = (from_tuple(i) for i in ((1, 7), (6, 7)))
    enemy_poses = (from_tuple(i) for i in ((1, 0), (6, 0)))


class Queen:
    name = 'queen'
    user_poses = (Vector2(3, 7), )
    enemy_poses = (Vector2(3, 0), )


class King:
    name = 'king'
    user_poses = (Vector2(4, 7), )
    enemy_poses = (Vector2(4, 0), )
