import pygame
from . import game


class MessageCommunication:
    def init(self, go, font_size: int, chess_machine) -> None:
        self.go = go
        self.last_check_time = 0
        self.pending_req = None
        self.msg_surface = None
        self.font_size = font_size

    def set_msg(self, msg) -> None:
        base_font = pygame.font.Font(None, self.font_size)
        self.msg_surface = base_font.render(
            msg.text, False, pygame.color.THECOLORS['black'])
        game.screen.blit(self.msg_surface, self.go.position.to_tuple())

    def check_self_response(self, event) -> None:
        if event.type == pygame.K_UP:
            self.msg_com.send('OK', True)
        elif event.type == pygame.K_DOWN:
            self.msg_com.send('NO', True)

    def check_msg(self):
        time = pygame.time.get_time()
        interval = game.data['request-interval']
        if self.last_check_time + interval >= time:
            return

        self.last_check_time = time

        msg = game.clnt.get_msg()
        if not msg:
            return

        self.set_msg(msg['text'])
        self.handle_response(msg)
    
    def handle_response(self, msg):
        if msg['response']:
            if msg['text'] == 'OK':
                chess_machine
            


    def update(self):
        for event in game.events:
            self.check_self_response(event)
        self.check_msg()
