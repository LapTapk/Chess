import pygame
from . import game


class Button:
    def init(self, go, rend, *funcs):
        self.go = go
        self.rend = rend
        self.funcs = funcs

    def is_clicked(self):
        rect = self.rend.get_rect()

        m_pos = pygame.mouse.get_pos()
        over_button = rect.collidepoint(m_pos)
        mouse_down = any(event.type == pygame.MOUSEBUTTONDOWN
                         for event in game.events)

        return over_button and mouse_down

    def update(self):
        if not self.is_clicked():
            return

        for func in self.funcs:
            func()
