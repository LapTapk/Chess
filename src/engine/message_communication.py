import pygame
from typing import *
from . import game, game_object, chess_state_machine, renderer


class MessageCommunication:
    '''Компонент, отвечающий за восприятие сигналов отправки сообщений противнику 
    и вывод их на экран'''

    def init(self, go: game_object.GameObject, font_size: int, chess_machine: chess_state_machine.ChessStateMachine, rend: renderer.Renderer) -> None:
        '''Инициализатор. Аналогичен __init__. Все параметры соответствуют полям класса'''
        self.go: game_object.GameObject = go
        '''``GameObject``, к которому прикреплен компонент'''
        self.last_check_time: int = 0
        '''Время последней проверки наличия сообщения'''
        self.msg_surface: pygame.surface.Surface = None
        '''``Surface`` текста последнего сообщения'''
        self.chess_machine: chess_state_machine.ChessStateMachine = chess_machine
        '''``ChessStateMachine``, необходимый для переключения на конец игры'''
        self.cur_msg: Dict[LiteralString, LiteralString | bool] = None
        '''Последнее сообщение'''
        self.font_size: int = font_size
        '''Размер шрифта выводимого сообщния'''
        self.rend: renderer.Renderer = rend
        '''``Renderer``, с помощью которого будет выводится текст сообщения'''

    def show_msg(self, msg: Dict[LiteralString, LiteralString | bool]) -> None:
        '''Процедура, выводящая сообщение на экран

        :param msg: сообщение, которое необходимо вывести'''
        base_font = pygame.font.Font(None, self.font_size)
        msg_surface = base_font.render(
            msg, False, pygame.color.THECOLORS['black'])
        self.rend.img = msg_surface

    def handle_input(self, event: pygame.event.Event) -> None:
        '''
        Метод, обрабатывающий ввод игрока. 
        Стрелка вверх - сообщение о признании себя побежденным / да.
        Стрелка вниз - сообщение с предложением ничьи / нет

        :param event: событие, которое необходимо обработать.
        '''
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

    def check_msg(self) -> None:
        '''Метод, выполняющий проверку на наличие сообщения к себе
        через некий интервал времени.'''
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

    def handle_response(self, msg: Dict[LiteralString, LiteralString | bool]) -> None:
        '''Метод, обрабатывающий входящее сообщение.
        Если пришло сообщение с соглашением на ничью или с признанием поражения

        :param msg: сообщение, которое нужно обработать'''
        if msg['text'] == 'Ок' or msg['text'] == 'Сдаюсь':
            self.chess_machine.change_state(self.chess_machine.end_state)

    def update(self) -> None:
        '''Метод кадра компонента'''
        for event in game.events:
            self.handle_input(event)
        self.check_msg()
