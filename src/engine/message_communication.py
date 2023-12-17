import pygame
from . import game


class MessageCommunication:
    def init(self, go, font_size: int, chess_machine, rend) -> None:
        self.go = go
        self.last_check_time = 0
        self.msg_surface = None
        self.chess_machine = chess_machine
        self.cur_msg = None
        self.font_size = font_size
        self.rend = rend

    def show_msg(self, msg) -> None:
        base_font = pygame.font.Font(None, self.font_size)
        msg_surface = base_font.render(
            msg, False, pygame.color.THECOLORS['black'])
        self.rend.img = msg_surface

    def handle_input(self, event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        msg = ''
        if event.key == pygame.K_s:
            if self.cur_msg != None and not self.cur_msg['response']:
                msg = 'Ок'
                game.clnt.send_msg(msg, True)
            else:
                msg = 'Сдаюсь'
                game.clnt.send_msg(msg, False)
            self.handle_response({'text': 'Ок'})
        elif event.key == pygame.K_d:
            if self.cur_msg != None and not self.cur_msg['response']:
                msg = 'Нет'
                game.clnt.send_msg(msg, True)
            else:
                msg = 'Ничья?'
                game.clnt.send_msg(msg, False)

        self.show_msg(msg)

    def check_msg(self):
        time = pygame.time.get_ticks()
        interval = game.data['request-interval']
        if self.last_check_time + interval >= time:
            return

        self.last_check_time = time

        msg = game.clnt.get_msg()
        self.cur_msg = msg
        if not msg:
            return

        self.show_msg(msg['text'])
        self.handle_response(msg)

    def handle_response(self, msg):
        if msg['text'] == 'Ок' or msg['text'] == 'Сдаюсь':
            self.chess_machine.change_state(self.chess_machine.end_state)

    def update(self):
        for event in game.events:
            self.handle_input(event)
        self.check_msg()
