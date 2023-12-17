from .vector2 import *
from . import game, game_object
import pygame


class Renderer:
    '''Компонент, отвечающий за прорисовку изображения на экране'''
    def init(self, go: game_object.GameObject, img: pygame.surface.Surface) -> None:
        '''Инициализатор. Аналогичен __init__. Все параметры соответствуют полям класса'''
        self.img: pygame.surface.Surface = img
        '''Неизмененное изображение'''
        self.tmp_img: pygame.surface.Surface = img
        '''Изображение, измененное в соответствии с размерами экрана'''
        self.go: game_object.GameObject = go
        '''``GameObject``, которому принадлежит компонент'''

    def update(self) -> None:
        '''Метод кадра компонента'''
        self.__update_image()

        game.screen.blit(self.tmp_img, self.get_rect())

    def __update_image(self) -> None:
        '''Закрытый метод обновлния изображения в соответствии
        с размерами экрана'''
        scale = self.go.scale.to_tuple()
        rot = self.go.rotation

        self.tmp_img = pygame.transform.scale_by(self.img, scale)
        self.tmp_img = pygame.transform.rotate(self.tmp_img, rot)

    def get_rect(self) -> pygame.rect.Rect:
        '''Метод, обновляющий и возвращающий ``Rect`` 
        измененного изображения
        
        :return: ``Rect`` измененного изображения'''
        self.__update_image()

        img_rect = self.tmp_img.get_rect()
        img_size = Vector2(img_rect.w, img_rect.h)

        pos = self.go.position

        offset = pos - img_size / 2
        res = img_rect.move(offset.x, offset.y)

        return res
