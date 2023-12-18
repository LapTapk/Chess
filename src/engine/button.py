import pygame
from . import game, game_object, renderer
from typing import *


class Button:
    '''Компонент кнопки, выполняющей определенные действия при нажатии'''

    def init(self, go: game_object.GameObject, rend: renderer.Renderer, *funcs: Callable[[], None]):
        self.go: game_object.GameObject = go
        '''``GameObject`` к которому прикреплен компонент'''
        self.rend: renderer.Renderer = rend
        '''``Renderer`` с помощью которого кнопка выведется на экран'''
        self.funcs: Callable[[], None] = funcs
        '''События, которын должны произойти при нажатии кнопки'''

    def is_clicked(self) -> bool:
        '''Метод, проверяющий была ли нажата кнопка в данный кадр.

        :return: была ли кнопка нажата'''
        rect = self.rend.get_rect()

        m_pos = pygame.mouse.get_pos()
        over_button = rect.collidepoint(m_pos)
        mouse_down = any(event.type == pygame.MOUSEBUTTONDOWN
                         for event in game.events)

        return over_button and mouse_down

    def update(self) -> None:
        '''Метод кадра компонента'''
        if not self.is_clicked():
            return

        for func in self.funcs:
            func()
