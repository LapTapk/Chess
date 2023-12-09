from .vector2 import *
from . import game
import pygame


class Renderer:
    def init(self, go, img):
        self.img = img
        self.tmp_img = img
        self.go = go

    def update(self):
        self.__update_image()

        game.screen.blit(self.tmp_img, self.get_rect())

    def __update_image(self):
        scale = self.go.scale.to_tuple()
        rot = self.go.rotation

        self.tmp_img = pygame.transform.scale_by(self.img, scale)
        self.tmp_img = pygame.transform.rotate(self.tmp_img, rot)

    def get_rect(self):
        self.__update_image()

        img_rect = self.tmp_img.get_rect()
        img_size = Vector2(img_rect.w, img_rect.h)

        pos = self.go.position

        offset = pos - img_size / 2
        res = img_rect.move(offset.x, offset.y)

        return res
