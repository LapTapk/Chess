from vector2 import *
from grid import GridBinder
from grab import Grabable


class Board:
    def init(self, go, figures):
        self.go = go
        self.figures = [[None] * 8 for _ in range(8)]
        for figure in figures:
            figure_data = figure.get_component(FigureData)
            coord = figure_data.binder.coord
            self.figures[coord.x][coord.y] = figure_data

    def update(self):
        pass

    def move(self, frm, to):
        figure = self.figures[frm.x][frm.y]

        figure.binder.coord = to

        self.figures[frm.x][frm.y] = None
        self.figures[to.x][to.y] = figure
    
    def set_freedom_user(self, is_free):
        for figures_row in self.figures:
            for figure in figures_row:
                if figure == None or not figure.owned_by_user:
                    continue

                grabable = figure.go.get_component(Grabable)
                grabable.is_moveable = is_free


class FigureData:
    def init(self, go, owned_by_user, binder):
        self.go = go
        self.owned_by_user = owned_by_user
        self.binder = binder
    
    def update(self):
        pass
