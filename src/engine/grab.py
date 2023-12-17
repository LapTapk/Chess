from .grid import GridBinder, find_closest, Grid
import pygame
from .vector2 import *
from . import game, game_object
from typing import *


class Grabber:
    '''Компонент, двигающий объекты за курсором, если на них нажали, 
    и оставляющий их на месте после произведнных манипуляций.'''

    def init(self, go: game_object.GameObject) -> None:
        '''Инициализатор. Аналогичен __init__. Все параметры соответствуют полям класса'''
        self.go: game_object.GameObject = go
        '''``GameObject``, которому принадлежит компонент'''
        self.grabbed: Grabable | None = None
        '''Захваченный объект'''

    def try_grab(self) -> None:
        '''Метод, осуществляющий попытку захвата объекта под курсором, 
        если такой имеется.'''
        if self.grabbed != None:
            return

        mouse_pos = pygame.mouse.get_pos()

        gos = self.go.scene.at_point(mouse_pos)

        grabable = None
        for go in gos:
            grabable = go.get_component(Grabable)
            if grabable != None:
                break

        if grabable == None or not grabable.is_moveable:
            return

        grabable.moving = True
        self.grabbed = grabable

    def drop(self) -> None:
        '''Метод, оставляющий захваченный объект на месте'''
        if self.grabbed == None:
            return

        self.grabbed.moving = False
        self.grabbed = None


class Grabable:
    '''Компонент объекта, который может быть захвачен. 
    Двигает объект, если необходимо.'''

    def init(self, go: game_object.GameObject, is_moveable: bool = True):
        '''Инициализатор. Аналогичен __init__. Все параметры соответствуют полям класса.'''
        self.is_moveable: bool = is_moveable
        '''Состояние, показывающее можно ли двигать объект'''
        self.moving: bool = False
        '''Состояние, показывающее необходимо ли двигать объект за курсором'''
        self.go: game_object.GameObject = go
        '''``GameObject``, которому принадлежит компонент'''

    def update(self):
        '''Метод кадра компонента.'''
        if not self.moving or not self.is_moveable:
            return

        self.move_to_mouse()

    def move_to_mouse(self):
        '''Метод, перемещающий объект к курсору'''
        factor_x = game.screen_size[0] / game.data['default-screen-size'][0]
        factor_y = game.screen_size[1] / game.data['default-screen-size'][1]
        m_pos = pygame.mouse.get_pos()
        m_pos = Vector2(m_pos[0] / factor_x, m_pos[1] / factor_y)
        self.go.nonscaled_position = m_pos


class FigureGrabber(Grabber):
    '''Компонент, перемещающий фигуры. Дочерний класс ``Grabber``'''

    def init(self, go: game_object.GameObject, grd: Grid):
        self.grd: Grid = grd
        '''``Grid`` относительно которого осуществляется поиск ближайшей клетки, куда можно поставить фигуру'''
        self.grabbed_coord: Vector2 = None
        '''Относительная координата ``Grid`` размещения фигуры'''
        super().init(go)

    def __unbind(self) -> None:
        '''Закрытый метод, открепляющий фигуру от сетки'''
        grabbed = self.grabbed
        if grabbed == None:
            return

        binder = grabbed.go.get_component(GridBinder)
        binder.binded = False

    def try_grab(self) -> None:
        '''Метод, осуществляющий попытку захватить фигуру'''
        super().try_grab()

        if self.grabbed == None:
            return

        binder = self.grabbed.go.get_component(GridBinder)
        self.grabbed_coord = binder.coord
        self.__unbind()

    def get_move(self) -> Tuple[Vector2, Vector2]:
        '''Метод, возращающий потенциальный ход.

        :return: потенциальный ход, координата откуда была взята фигура, и куда ее можно поставить'''
        factor_x = game.screen_size[0] / game.data['default-screen-size'][0]
        factor_y = game.screen_size[1] / game.data['default-screen-size'][1]
        m_pos = pygame.mouse.get_pos()
        m_pos = Vector2(m_pos[0] / factor_x, m_pos[1] / factor_y)
        to = find_closest(self.grd, m_pos)
        frm = self.grabbed_coord

        return frm, to
