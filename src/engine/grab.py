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

    def next_move(self):
        '''
        Decides what grabber can do next.
        If something is grabbed grabber drops it.
        If nothing is grabbed grabber tries to grab something
        '''
        if self.grabbed == None:
            self.__try_grab()
        else:
            self.__drop()

    def __try_grab(self):
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

    def __drop(self):
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
    def __init__(self):
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
