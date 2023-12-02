class ChessStateManager:
    def init(self, go, first_state):
        self.go = go
        self.cur_state = first_state

    def update(self):
        self.cur_state.update()

    
        