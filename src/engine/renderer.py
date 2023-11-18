from vector2 import *
import game
import pygame


class Renderer:
    '''
    A ``component`` for game object, that contains and displas its sprite.

    :param pygame.Surface screen: sets *screen* field
    :param pygame.Surface img: sets *img* field
    '''

    def __init__(self, img):
        self.img = img
        self.tmp_img = img
        '''Surface of a sprite'''
        self.go = None
        '''Game object renderer is attached to'''

    def update(self):
        '''
        ``Component`` method.
        Displays sprite
        '''
        self.__update_image()

        game.screen.blit(self.tmp_img, self.get_rect())

    def __update_image(self):
        '''
        Method that sets sprite to state in pygame plane that
        go has
        '''
        scale = self.go.scale.to_tuple()
        rot = self.go.rotation

        self.tmp_img = pygame.transform.scale_by(self.img, scale)
        self.tmp_img = pygame.transform.rotate(self.tmp_img, rot)

    def get_rect(self):
        '''
        :rtype: Vector2
        :return: rect of the image corelated to ``game object`` renderer
        is attached to
        '''
        img_rect = self.tmp_img.get_rect()
        img_size = self.tmp_img.get_size()

        pos = self.go.position

        offset = pos - from_tuple(img_size) / 2
        return img_rect.move(offset.to_tuple())
