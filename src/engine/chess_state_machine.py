import pygame
import game


class ChessStateMachine:
    def init(self, go, first_state):
        self.go = go
        self.cur_state = None
        self.change_state(first_state)

    def change_state(self, new_state):
        if self.cur_state != None:
            self.cur_state.on_exit()
        self.cur_state = new_state
        self.cur_state.on_start()

    def update(self):
        self.cur_state.update()


class UserTurnState:
    def init(self, machine, grabber):
        self.machine = machine
        self.grabber = grabber

    def on_start(self):
        self.grabber.brd.set_freedom_user(True)

    def on_exit(self):
        self.grabber.brd.set_freedom_user(False)

    def handle_input(self):
        for event in game.events:
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            grabber = self.grabber
            if grabber.grabbed == None:
                grabber.try_grab()
            else:
                success = grabber.try_drop()
                if success:
                    self.machine.change_state(EnemyTurnState())

    def update(self):
        self.handle_input()


class EnemyTurnState:
    def on_start(self):
        pass

    def on_exit(self):
        pass

    def update(self):
        pass
