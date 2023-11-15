import pygame
from vector2 import *


class Grabber:
    def __init__(self, scene):
        self.scene = scene
        self.grabbed = None

    def next_move(self):
        if self.grabbed == None:
            self.__try_grab()
        else:
            self.__drop()


    def __try_grab(self):
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
        self.grabbed.moving = False
        self.grabbed = None
       
        
class Grabable:
    def __init__(self):
        self.moving = False
        self.go = None

    def update(self):
        if not self.moving:
            return
        
        self.move_to_mouse()

    def move_to_mouse(self):
        mpos = pygame.mouse.get_pos()
        self.go.position = from_tuple(mpos)