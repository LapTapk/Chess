import pygame
import typing
from . import game, game_object, grab, board


class ChessStateMachine:
    '''
    Компонент, определяющий поведение в зависимости от текущего хода.
    '''

    def init(self, go: game_object.GameObject, grabber: grab.Grabber, brd_updater: board.BoardUpdater) -> None:
        '''Инициализатор. Аналогичен __init__. Все параметры соответствуют полям класса.'''
        self.go: game_object.GameObject = go
        '''``GameObject``, которому принадлежит текущий компонент.'''
        self.cur_state: [UserTurnState | EnemyTurnState] = None
        '''Текущее состояние сущности.'''
        self.user_turn_state: UserTurnState = UserTurnState(
            self, grabber, brd_updater)
        '''Состояние хода пользователя.'''
        self.enemy_turn_state: EnemyTurnState = EnemyTurnState(
            self, brd_updater)
        '''Состояние хода противника'''
        first_state = self.user_turn_state if game.clnt.is_white else self.enemy_turn_state
        self.change_state(first_state)

    def change_state(self, new_state) -> None:
        '''
        Процедура смены состояния.

        :param new_state: новое состояние.
        :type new_state: [UserTurnState | EnemyTurnState]
        '''
        self.cur_state = new_state
        self.cur_state.on_start()

    def update(self) -> None:
        '''Процедура обновления компонента для каждого кадра.'''
        self.cur_state.update()


class UserTurnState:
    '''
    Сущность состояния во время хода игрока. 
    Обрабатывает поднятие фигуры, обновление доски и передачу хода противнику.
    '''

    def __init__(self, machine: ChessStateMachine, grabber: grab.Grabber, brd_updater: board.BoardUpdater) -> None:
        self.machine = machine
        '''``ChessStateMachine`` в котором вызывается данное состояние.'''
        self.grabber = grabber
        '''``Grabber``, ответственный за поднятие фигур с доски.'''
        self.brd_updater = brd_updater
        '''Средство обновления выводимой доски.'''

    def on_start(self) -> None:
        '''
        Метод, вызываемый при обновлении состояния машиной.
        Для ``UserTurnState`` обновляет доску.
        '''
        brd = game.clnt.get_board()
        self.brd_updater.update_board(brd, game.clnt.is_white, True)

    def handle_input(self) -> None:
        '''
        Метод, обрабатывающий входные *event*.
        Если ни одна фигура не поднята, то пытается поднять.
        Если фигура ставится на стол, спрашивает у сервера легальность 
        хода.
        '''
        for event in game.events:
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            grabber = self.grabber
            if grabber.grabbed == None:
                grabber.try_grab()
            else:
                frm, to = map(lambda x: x.to_tuple(), grabber.get_move())
                success = game.clnt.send_move(frm, to)
                if success:
                    self.machine.change_state(self.machine.enemy_turn_state)
                    grabber.grabbed = None

    def update(self) -> None:
        '''Процедура кадра, вызываемая ``ChessStateMachine``'''
        self.handle_input()


class EnemyTurnState:
    '''
    Сущность состояния хода противника.
    Ожидает, посылая время от времени запросы, пока противник на другом клиенте сходит, 
    и передает ход пользователю.
    '''

    def __init__(self, machine: ChessStateMachine, brd_updater: board.BoardUpdater) -> None:
        self.machine: ChessStateMachine = machine
        '''``ChessStateMachine`` в котором вызывается данное состояние.'''
        self.clock: pygame.time.Clock() = pygame.time.Clock()
        '''Таймер для отсчета времени следующего запроса.'''
        self.request_interval: int = game.data['request-interval']
        '''Интервал запросa'''
        self.brd_updater: board.BoardUpdater = brd_updater
        '''Средство обновления выводимой доски.'''
        self.last_check_time: int = 0
        '''Время последнего запросa'''

    def on_start(self) -> None:
        '''
        Метод, вызываемый при обновлении состояния машиной.
        Обновляет доску.
        '''
        brd = game.clnt.get_board()
        self.brd_updater.update_board(brd, game.clnt.is_white, False)

    def update(self) -> None:
        '''
        Процедура кадра, вызываемая ``ChessStateMachine``.
        Проверяет, когда был послан последний запрос, и если 
        пришло время нового запроса, передает ход пользователю.
        '''
        time = pygame.time.get_ticks()
        if self.last_check_time + self.request_interval > time:
            return

        self.last_check_time = time

        has_moved = game.clnt.has_moved()
        if not has_moved:
            return

        self.machine.change_state(self.machine.user_turn_state)
