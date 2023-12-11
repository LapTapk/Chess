import pygame
from . import game


class InputBox:
    def init(self, go, font_size, invitation):
        self.go = go
        self.text = ''
        self.font_size = font_size
        self.invitation = invitation


    def handle_input(self):
        for event in game.events:
            if event.type != pygame.KEYDOWN:
                continue
            
            text_is_invitation = self.text == self.invitation
            if text_is_invitation:
                self.text = ''

            if event.key == pygame.K_BACKSPACE:
                if not text_is_invitation:
                    self.text = self.text[:-1]
                continue

            self.text += event.unicode


    def show_text(self):
        base_font = pygame.font.Font(None, self.font_size)
        text_surface = base_font.render(self.text, True, (0, 0, 0))
        gopos = self.go.position.to_tuple()
        game.screen.blit(text_surface, gopos)

    
    def update(self):
        if self.text == '':
            self.text = self.invitation

        self.handle_input()
        self.show_text()