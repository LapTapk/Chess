import pygame
from . import game


class ChessStateMachine:
    def init(self, go, grabber, brd_updater):
        self.go = go
        self.cur_state = None
        self.user_turn_state = UserTurnState(self, grabber, brd_updater)
        self.enemy_turn_state = EnemyTurnState(self, brd_updater)
        first_state = self.user_turn_state if game.clnt.is_white else self.enemy_turn_state
        self.change_state(first_state)

    def change_state(self, new_state):
        self.cur_state = new_state
        self.cur_state.on_start()

    def update(self):
        self.cur_state.update()


class UserTurnState:
    def __init__(self, machine, grabber, brd_updater):
        self.machine = machine
        self.grabber = grabber
        self.brd_updater = brd_updater

    def on_start(self):
        brd = game.clnt.get_board()
        self.brd_updater.update_board(brd, game.clnt.is_white, True)

    def handle_input(self):
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

    def update(self):
        self.handle_input()


class EnemyTurnState:
    def __init__(self, machine, brd_updater):
        self.machine = machine
        self.clock = pygame.time.Clock()
        self.request_interval = game.data['request-interval']
        self.brd_updater = brd_updater
        self.last_check_time = 0

    def on_start(self):
        brd = game.clnt.get_board()
        self.brd_updater.update_board(brd, game.clnt.is_white, False)

    def update(self):
        time = pygame.time.get_ticks()
        if  self.last_check_time + self.request_interval > time:
            return 

        self.last_check_time = time

        has_moved = game.clnt.has_moved()
        if not has_moved:
            return

        self.machine.change_state(self.machine.user_turn_state)
