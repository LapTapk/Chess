import grab
from grid import GridBind
import pygame
from vector2 import *


class Grabber:
    '''
    Entity that manages grabbing objects
    TODO: add params
    '''

    def __init__(self, scene):
        self.scene = scene
        '''
        ``Scene`` where search for grabable object is being done
        '''
        self.grabbed = None
        '''
        Grabbed object. None if no object if grabbed
        '''

    def try_grab(self):
        '''
        Finds grabable objects under cursor anf tries to grab it
        '''
        if self.grabbed != None:
            return

        mouse_pos = pygame.mouse.get_pos()

        gos = self.scene.at_point(mouse_pos)

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
        '''
        If something is grabbed then drop it
        '''
        if self.grabbed == None:
            return

        self.grabbed.moving = False
        self.grabbed = None


class Grabable:
    '''
    ``Component`` that indicates that this object can be 
    moved and moves it
    TODO: add params
    '''

    def __init__(self, is_moveable=True):
        self.is_moveable = is_moveable
        '''Defines if object can be grabbed and moved'''
        self.moving = False
        '''Tells if object needs to move'''
        self.go = None
        '''``GameObject`` this component is attached to'''

    def update(self):
        '''``Component``'s method'''
        if not self.moving:
            return

        self.move_to_mouse()

    def move_to_mouse(self):
        '''
        Moves *game object* after the mouse
        '''
        mpos = pygame.mouse.get_pos()
        self.go.position = from_tuple(mpos)


class FigureGrab:
    def __init__(self, scene, board_grid, grabber):
        self.scene = scene
        self.board_grid = board_grid
        self.grabber = grabber

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

    def try_bind(self):
        grabbed = self.grabber.grabbed 
        if grabbed == None:
            return

        binder = grabbed.go.get_component(GridBind)
        binder.binded = False

    def unbind(self):
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
        self.try_bind()
    

    def drop(self):
        self.unbind()
        self.grabber.drop()
