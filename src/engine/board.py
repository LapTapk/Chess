from grid import GridBinder


class Board:
    def init(self, go, grid):
        self.go = go
        self.grid = grid
        self.figures = self.create_figures()

    def create_figures():
        #TODO: figures gos
        pass

    def move(self, frm, to):
        figure = self.figures[frm.x][frm.y]

        binder = figure.get_component(GridBinder)
        binder.coord(to.x, to.y)

        self.figures[frm.x][frm.y] = None
        self.figures[to.x][to.y] = figure
