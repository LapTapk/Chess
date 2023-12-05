import game
from grid import GridBinder, find_closest
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


class GridGrabber(Grabber):
    def init(self, go, grid):
        self.grid = grid
        super().init(go)

    def __unbind(self):
        grabbed = self.grabbed
        if grabbed == None:
            return

        binder = grabbed.go.get_component(GridBinder)
        binder.binded = False

    def __try_bind(self, grid_pos):
        if self.grabbed == None:
            return

        binder = self.grabbed.go.get_component(GridBinder)
        if binder != None:
            binder.coord = grid_pos
            binder.binded = True

    def try_grab(self):
        super().try_grab()
        self.__unbind()

    def drop(self, grid_pos):
        self.__try_bind(grid_pos)
        self.grabbed = None
        super().drop()

    def update(self):
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.grabber.grabbed == None:
                    self.try_grab()
                else:
                    m_pos = pygame.mouse.get_pos()
                    self.drop(find_closest(self.grid, m_pos))


class FigureGrabber(GridGrabber):
    def init(self, go, board_grid, board):
        self.board = board
        self.grabbed_coord = None
        super().init(go, board_grid)

    def try_grab(self):
        super().try_grab() 

        if self.grabbed == None:
            return 

        binder = self.grabbed.go.get_component(GridBinder)
        self.grabbed_coord = binder.coord

    def try_drop(self):
        m_pos = from_tuple(pygame.mouse.get_pos())
        to = find_closest(self.grid, m_pos)
        frm = self.grabbed_coord

        can_drop = self.board.valid(frm, to)
        if not can_drop:
            return False, frm, to
        
        super().drop(to)
        self.grabbed_coord = None
        return True, frm, to
    
    def update(self):
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.grabbed == None:
                    self.try_grab()
                else:
                    self.try_drop()
            