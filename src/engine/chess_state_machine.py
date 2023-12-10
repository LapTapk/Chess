import pygame
from . import game


class ChessStateMachine:
    def init(self, go, grabber, brd_updater):
        self.go = go
        self.cur_state = None
        self.user_turn_state = UserTurnState(self, grabber, brd_updater)
        self.enemy_turn_state = EnemyTurnState(self, brd_updater)
        self.change_state(self.user_turn_state)

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
        brd = game.client.try_get_board()
        self.brd_updater.update_board(brd, True, game.client.is_white)

    def handle_input(self):
        for event in game.events:
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            grabber = self.grabber
            if grabber.grabbed == None:
                grabber.try_grab()
            else:
                frm, to = grabber.get_move()
                success = game.client.send_move(frm, to)
                if success:
                    self.machine.change_state(self.machine.enemy_turn_state)

    def update(self):
        self.handle_input()


class EnemyTurnState:
    def __init__(self, machine, brd_updater):
        self.machine = machine
        self.clock = pygame.time.Clock()
        self.request_interval = game.data['request-interval']
        self.brd_update = brd_updater

    def on_start(self):
        brd = game.client.try_get_board()
        self.brd_updater.update_board(brd, game.client.is_white, False)

    def update(self):
        delta_time = self.clock.tick()
        if delta_time < self.request_interval:
            return 

        has_moved = game.client.has_moved()
        if has_moved:
            return

        self.machine.change_state(self.machine.user_turn_state)
