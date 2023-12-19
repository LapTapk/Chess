from . import game_object, renderer, grab, grid, game
from .vector2 import *
import pygame
from typing import *
import chessLogic.Board


class BoardUpdater:
    '''Компонент, отвечающий за обновление доски в 
    соотвествии с определенной доской из *chessLogic*'''

    def init(self, go: game_object.GameObject, grd: grid.Grid):
        '''Инициализатор. Аналогичен __init__. Все параметры соответствуют полям класса.'''
        self.go: game_object.GameObject = go
        '''``GameObject``, которому принадлежит компонент'''
        self.grd: grid.Grid = grd
        '''``Grid``, относительно которого будет строиться новая доска при обновлении'''

    def create_figure(self, scene: game_object.Scene, coord: Vector2,
                      name: LiteralString, owned_by_user: bool, is_user_free: bool) -> None:
        '''Метод, создающий фигуру

        :param scene: сцена, на которой будет располагаться фигура 
        :param coord: относительная координата сетки, где будет располагаться фигура
        :param name: название фигуры
        :param owned_by_user: состояние, означающее, принадлежит ли фигура пользователю
        :param is_user_free: состояние, означающее, сейчас ли ход пользователя
        '''
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

    def create_figures(self, board: chessLogic.Board.Board, is_white: bool, is_user_free: bool):
        '''Создает весь необходимый набор фигур 

        :param board: логическая доска, по которой строится доска для пользователя
        :param is_white: состояние, показывающее, играет ли за белых пользватель
        :param is_user_free: состояние, показывающее, ход ли сейчас пользователя'''
        user_color = 'white' if is_white else 'black'
        res = []
        for i in range(8):
            for j in range(8):
                figure = board.board[i][j]
                if figure.name == '.':
                    continue

                coord = Vector2(i, j)
                if user_color == 'white':
                    if figure.name not in 'kqKQ':
                        coord = Vector2(7, 7) - coord
                    else:
                        coord = Vector2(coord.x, 7 - coord.y)
                else:
                    if figure.name in 'kqKQ':
                        coord = Vector2(7 - coord.x, coord.y)

                scene = self.go.scene
                owned_by_user = user_color == figure.color
                figure_go = self.create_figure(scene, coord, figure.name,
                                               owned_by_user, is_user_free)
                res.append(figure_go)
        return res

    def update_board(self, board, is_white, is_user_free):
        '''Процедура, обновляющая доску

        :param board: логическая доска, по которой будет строиться пользовательская доска
        :param is_white: состояние, показывающее, играет ли за белых пользватель
        :param is_user_free: состояние, показывающее, ход ли сейчас пользователя'''
        figures = self.create_figures(board, is_white, is_user_free)
        self.go.children = figures

    def update(self):
        '''Пустой метод кадра компонента'''
        pass


class FigureData:
    '''Вспомогательный компонент, содержащий некоторые характеристики фигуры.'''

    def init(self, go: game_object.GameObject, binder: grid.GridBinder):
        '''Инициализатор. Аналогичен __init__. Все параметры соответствуют полям класса'''
        self.go: game_object.GameObject = go
        '''``GameObject``, которму принадлежит компонент'''
        self.binder: grid.GridBinder = binder
        '''``Binder``, закрепляющий фигуру за клеткой'''

    def update(self):
        '''Пустой метод кадра компонента'''
        pass
