import game
from grid import GridBind
import pygame
from vector2 import *


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

        if grabable == None:
            return

        grabable.moving = True
        self.grabbed = grabable

    def drop(self):
        if self.grabbed == None:
            return

        self.grabbed.moving = False
        self.grabbed = None

    def update(self):
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.grabbed == None:
                    self.try_grab()
                else:
                    self.drop()


class Grabable:

    def init(self, go, is_moveable=True):
        self.is_moveable = is_moveable
        self.moving = False
        self.go = go

    def update(self):
        if not self.moving:
            return

        self.move_to_mouse()

    def move_to_mouse(self):
        mpos = pygame.mouse.get_pos()
        self.go.position = from_tuple(mpos)


class GridGrab:
    def init(self, go, board_grid):
        self.go = go
        self.board_grid = board_grid

        self.grabber = Grabber()
        self.grabber.init(go)

    def __find_closest(self, go):
        pts = self.board_grid.get_points()
        res = Vector2(0, 0)

        for i in range(len(pts)):
            for j in range(len(pts[0])):
                new_point = pts[i][j]
                cur_point = pts[res.x][res.y]
                cur = cur_point - go.position
                new = new_point - go.position
                if cur.length() > new.length():
                    res = Vector2(i, j)

        return res

    def unbind(self):
        grabbed = self.grabber.grabbed
        if grabbed == None:
            return

        binder = grabbed.go.get_component(GridBind)
        binder.binded = False

    def try_bind(self):
        grabbed = self.grabber.grabbed
        if grabbed == None:
            return

        closest = self.__find_closest(grabbed.go)

        binder = grabbed.go.get_component(GridBind)
        if binder != None:
            binder.coord = closest
            binder.binded = True

    def try_grab(self):
        self.grabber.try_grab()
        self.unbind()

    def drop(self):
        self.try_bind()
        self.grabber.drop()

    def update(self):
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.grabber.grabbed == None:
                    self.try_grab()
                else:
                    self.drop()
