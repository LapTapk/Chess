import pygame
from vector2 import Vector2


class CursorMove:
    '''
    ``Component`` that moves ``game object`` with the cursor

    :param bool moving: sets initial moving field
    '''

    def __init__(self, moving=False):
        self.go = None
        '''``Game object`` that ``component`` is attached to'''
        self.moving = moving
        '''Tells if *game object* needs to move with cursor'''

    def update(self):
        '''``Component`` method. Moves *game object* if necessary'''
        if not self.moving:
            return

        self.move()

    def move(self):
        '''Sets *game object's* position to cursor position'''
        mouse_pos = pygame.mouse.get_pos()
        self.go.position = Vector2.from_tuple(mouse_pos)
