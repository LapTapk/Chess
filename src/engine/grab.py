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


class GridGrabber:
    def init(self, go, grid):
        self.go = go
        self.grid = grid
        self.grabbed = None

        self.grabber = Grabber()
        self.grabber.init(go)

    def __unbind(self):
        grabbed = self.grabber.grabbed
        if grabbed == None:
            return

        binder = grabbed.go.get_component(GridBind)
        binder.binded = False

    def __try_bind(self, grid_pos):
        if self.grabbed == None:
            return

        binder = self.grabbed.go.get_component(GridBind)
        if binder != None:
            binder.coord = grid_pos
            binder.binded = True

    def try_grab(self):
        self.grabber.try_grab()
        self.grabbed = self.grabber.grabbed
        self.__unbind()

    def drop(self, grid_pos):
        self.__try_bind(grid_pos)
        self.grabbed = None
        self.grabber.drop()

    def update(self):
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.grabber.grabbed == None:
                    self.try_grab()
                else:
                    m_pos = pygame.mouse.get_pos()
                    self.drop(find_closest(self.grid, m_pos))


class FigureGrabber:
    def init(self, go, board_grid, board):
        self.go = go
        self.grabber = GridGrabber()
        self.board = board
        self.grabbed_coord = None
        self.grabbed = None

        self.grabber.init(go, board_grid)

    def try_grab(self):
        self.grabber.try_grab()
        self.grabbed = self.grabber.grabbed

        if self.grabbed == None:
            return 

        binder = self.grabbed.go.get_component(GridBind)
        self.grabbed_coord = binder.coord

    def try_drop(self):
        m_pos = from_tuple(pygame.mouse.get_pos())
        to = find_closest(self.grabber.grid, m_pos)
        frm = self.grabbed_coord

        can_drop = self.board.valid(frm, to)
        if not can_drop:
            return False, frm, to
        
        self.grabber.drop(to)
        self.grabbed = None
        self.grabbed_coord = None
        return True, frm, to
    
    def update(self):
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.grabber.grabber.grabbed == None:
                    self.try_grab()
                else:
                    self.try_drop()
            