import pygame
from . import game_object
from . import game
from typing import *


class InputBox:
    '''
    Компонент, отвечающий за ввод текстовых данных. 
    Считывает и показывает введенные символы
    только тогда, когда пользователь активировал 
    ввод нажатием пкм на текстовое окно.
    В случае, если вводимая строка пуста, выводит 
    строку с приглашением к вводу.
    '''

    def init(self, go: game_object.GameObject, font_size: int, invitation: LiteralString, is_valid: Callable[[Literal], bool], rend) -> None:
        '''
        Инициализатор. Аналогичен __init__. 
        Все параметры соответствуют полям класса.
        '''
        self.go: game_object.GameObject = go
        '''``GameObject``, к которому прикреплен компонент.'''
        self.text: LiteralString = ''
        '''Введенный текст.'''
        self.font_size: int = font_size
        '''Размер шрифта выводимого текста.'''
        self.invitation: LiteralString = invitation
        '''Строка, приглашающая к написанию текста.'''
        self.active: bool = False
        '''Состояние, показывающее, активна ли строка ввода.'''
        self.is_valid: Callable[[Literal], bool] = is_valid
        '''Функция проверки правильности вводимых символов.'''
        self.surface: pygame.surface.Surface = None
        '''``Surface``, используемая для вывода текста.'''
        self.rend = rend

    def handle_text_input(self, event: pygame.event.Event) -> None:
        '''
        В зависимости от введенного символа выполняет действия:
        1. если K_BACKSPACE, то удаляет последний символ.
        2. иначе проверяет легальность символа и вносит его в *self.text*. 

        :param event: событие, которое необходимо обработать.
        '''
        text_is_invitation = self.text == self.invitation
        if text_is_invitation:
            self.text = ''

        char = event.unicode

        if event.key == pygame.K_BACKSPACE:
            if not text_is_invitation:
                self.text = self.text[:-1]
        elif self.is_valid(char):
            self.text += char

    def handle_activation(self) -> None:
        '''
        Провеяет активацию через нажатие ПКМ.
        '''
        m_pos = pygame.mouse.get_pos()
        rect = self.rend.get_rect()

        self.active = rect.collidepoint(m_pos)

    def handle_input(self) -> None:
        '''
        Совокупность *handle_activation* и *handle_text_input* c соответсвующии им 
        событиями
        '''
        for event in game.events:
            if self.active and event.type == pygame.KEYDOWN:
                self.handle_text_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_activation()

    def show_text(self) -> None:
        '''
        Выводит текст на экран.
        '''
        base_font = pygame.font.Font(None, self.font_size)
        surface = base_font.render(self.text, True, (0, 0, 0))
        self.rend.img = surface

    def update(self) -> None:
        '''Функция кадра компонента, выполняющая его функционал.'''
        if self.text == '':
            self.text = self.invitation

        self.show_text()
        self.handle_input()
