from . import game_object, renderer, grab, grid, game
from .vector2 import *
from chessLogic.Board import Board
import pygame


class BoardUpdater:
    def init(self, go, grd):
        self.go = go
        self.grd = grd

    def create_figure(self, scene, coord,
                      name, owned_by_user, is_user_free):
        go = game_object.GameObject()
        rend = renderer.Renderer()
        grabable = grab.Grabable()
        binder = grid.GridBinder()
        figure_data = FigureData()
        img = pygame.image.load(game.data[name]).convert_alpha()
        rend.init(go, img)
        grabable.init(go, owned_by_user and is_user_free)
        binder.init(go, self.grd, coord)
        figure_data.init(go, binder)
        go.init(scene, components=[rend, grabable, binder, figure_data])
        return go

    def create_figures(self, board, user_color, is_user_free):
        res = []
        for i in range(Board.lenght):
            for j in range(Board.lenght):
                figure = board.board[i][j]
                if figure.name == '.':
                    continue

                coord = Vector2(i, j)
                if user_color == 'white':
                    coord.y = Board.lenght - coord.y - 1

                scene = self.go.scene
                owned_by_user = user_color == figure.color
                figure_go = self.create_figure(scene, coord, figure.name,
                                               owned_by_user, is_user_free)
                res.append(figure_go)
        return res

    def update_board(self, board, user_color, is_user_free):
        figures = self.create_figures(board, user_color, is_user_free)
        self.go.children = figures

    def update(self):
        pass


class FigureData:
    def init(self, go, binder):
        self.go = go
        self.binder = binder

    def update(self):
        pass
