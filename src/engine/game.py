'''Главный модуль движка. Ядро исполнения программы'''

import json
from . import game_object
from chess_server import client
import pygame
from typing import *

screen: pygame.surface.Surface = None
'''Главный экран.'''
clock: pygame.time.Clock = None
'''Часы для отмерки fps.'''
is_running: bool = False
'''Состояние, показывающее, идет ли игра.'''
screen_size: Tuple[int, int] = None
'''Размер главного экрана.'''
fps: int = None
'''Число кадров в секунду в игре.'''
cur_scene: game_object.Scene = None
'''Текущая главная ``Scene``.'''
is_init: bool = False
'''Состояние, показывающее инициализирована ли ``game``.'''
data: Dict[LiteralString, Any] = None
'''Характеристики игры по умолчанию'''
events: List[pygame.event.Event] = None
'''События, произошедшие за последний кадр.'''
clnt: client.Client = None
'''Клиент, который будет обмениваться информацией с сервером.'''


def init(scr_size: Tuple[int, int], fps_in: int, data_json_path: LiteralString) -> None:
    '''
    Инициализатор ``game``. Все параметры соответствуют полям модуля.
    '''
    global screen, clock, running, is_init
    global fps, cur_scene, screen_size
    global data

    if is_init:
        raise Exception("Game is already initialized")

    pygame.init()
    screen = pygame.display.set_mode(scr_size)
    clock = pygame.time.Clock()

    running = False
    screen_size = scr_size
    fps = fps_in
    cur_scene = None

    is_init = True

    with open(data_json_path) as f:
        data = json.load(f)


def run() -> None:
    '''
    Процедура запуска игры.
    '''
    global running
    if not is_init:
        raise Exception('Game is not initialized')

    running = True

    while running:
        __iteration()


def change_screen_size(size: Tuple[int, int]) -> None:
    '''
    Процедура, изменяющая размер экрана.

    :param size: новый размер экрана
    '''
    global screen, screen_size
    screen_size = size
    screen = pygame.display.set_mode(size)


def check_for_exit() -> None:
    '''
    Процедура, проверяющая, не было ли вызвано закрытие окна.
    '''
    global running

    for event in events:
        if event.type == pygame.QUIT:
            running = False


def __iteration() -> None:
    '''
    Процедура одного кадра игры.
    '''
    global events
    events = pygame.event.get()

    check_for_exit()

    screen.fill((0, 0, 0))

    cur_scene.update()

    pygame.display.update()
    clock.tick(fps)
