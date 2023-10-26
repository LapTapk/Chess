from vector2 import Vector2
import pygame


class Renderer:
    '''
    A ``component`` for game object, that contains and displas its sprite.

    :param pygame.Surface screen: sets *screen* field
    :param pygame.Surface img: sets *img* field
    '''

    def __init__(self, screen, img):
        self.screen = screen
        '''Surface where sprite can be displayed'''
        self.img = img
        '''Surface of a sprite'''
        self.go = None
        '''Game object renderer is attached to'''

    def update(self):
        '''
        ``Component`` method.
        Displays sprite
        '''
        self.screen.fill((0, 0, 0))

        self.__update_image()

        offset = Vector2.from_tuple(self.img.get_rect().center)
        pos = self.go.position - offset

        self.screen.blit(self.img, pos.to_tuple())

    def __update_image(self):
        '''
        Method that sets sprite to state in pygame plane that
        go has
        '''
        scale = self.go.scale.to_tuple()
        rot = self.go.rotation

        self.img = pygame.transform.scale_by(self.img, scale)
        self.img = pygame.transform.rotate(self.img, rot)
