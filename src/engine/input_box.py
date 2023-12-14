import pygame
from . import game


class InputBox:
    def init(self, go, font_size, invitation):
        self.go = go
        self.text = ''
        self.font_size = font_size
        self.invitation = invitation
        self.active = False
        self.surface = None

    def handle_text_input(self, event):
        text_is_invitation = self.text == self.invitation
        if text_is_invitation:
            self.text = ''

        char = event.unicode

        if event.key == pygame.K_BACKSPACE:
            if not text_is_invitation:
                self.text = self.text[:-1]
        elif char.isdigit() or char == '.':
            self.text += event.unicode

    def handle_activation(self):
        m_pos = pygame.mouse.get_pos()
        go_pos = self.go.position
        rect = self.surface.get_rect().move(go_pos.x, go_pos.y)

        self.active = rect.collidepoint(m_pos)

    def handle_input(self):
        for event in game.events:
            if self.active and event.type == pygame.KEYDOWN:
                self.handle_text_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_activation()

    def show_text(self):
        base_font = pygame.font.Font(None, self.font_size)
        self.surface = base_font.render(self.text, True, (0, 0, 0))
        gopos = self.go.position.to_tuple()
        game.screen.blit(self.surface, gopos)

    def update(self):
        if self.text == '':
            self.text = self.invitation

        self.show_text()
        self.handle_input()
