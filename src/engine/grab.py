from .grid import GridBinder, find_closest
import pygame
from .vector2 import *
from . import game


class Grabber:
    def init(self, go):
        self.go = go
        self.grabbed = None

    def try_grab(self):
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

    def try_drop(self):
        if self.grabbed == None:
            return

        self.grabbed.moving = False
        self.grabbed = None


class Grabable:
    def init(self, go, is_moveable=True):
        self.is_moveable = is_moveable
        self.moving = False
        self.go = go

    def update(self):
        if not self.moving or not self.is_moveable:
            return

        self.move_to_mouse()

    def move_to_mouse(self):
        factor_x = game.screen_size[0] / game.data['default-screen-size'][0]
        factor_y = game.screen_size[1] / game.data['default-screen-size'][1]
        m_pos = pygame.mouse.get_pos()
        m_pos = Vector2(m_pos[0] / factor_x, m_pos[1] / factor_y)
        self.go.nonscaled_position = m_pos


class FigureGrabber(Grabber):
    def init(self, go, grd):
        self.grd = grd
        self.grabbed_coord = None
        super().init(go)

    def __unbind(self):
        grabbed = self.grabbed
        if grabbed == None:
            return

        binder = grabbed.go.get_component(GridBinder)
        binder.binded = False

    def try_grab(self):
        super().try_grab()

        if self.grabbed == None:
            return

        binder = self.grabbed.go.get_component(GridBinder)
        self.grabbed_coord = binder.coord
        self.__unbind()

    def get_move(self):
        factor_x = game.screen_size[0] / game.data['default-screen-size'][0]
        factor_y = game.screen_size[1] / game.data['default-screen-size'][1]
        m_pos = pygame.mouse.get_pos()
        m_pos = Vector2(m_pos[0] / factor_x, m_pos[1] / factor_y)
        to = find_closest(self.grd, m_pos)
        frm = self.grabbed_coord

        return frm, to
