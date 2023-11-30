import pygame
import renderer
import game


class Button:
    def init(self, go, *funcs):
        self.go = go
        self.funcs = funcs

    def is_clicked(self):
        rend = self.go.get_component(renderer.Renderer)
        rect = rend.get_rect()

        m_pos = pygame.mouse.get_pos()
        over_button = rect.collidepoint(m_pos)
        mouse_down = False
        for event in game.events:
            mouse_down |= event.type == pygame.MOUSEBUTTONDOWN
        
        return over_button and mouse_down
         

    def update(self):
        if not self.is_clicked():
            return

        for func in self.funcs:
            func()
