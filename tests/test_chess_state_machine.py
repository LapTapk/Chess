import utils
from src.engine import chess_state_machine as state_machine
from src.engine import game_object
import unittest.mock as mock


utils.game_pseudoinit()


def test_change_state():
    machine = state_machine.ChessStateMachine()
    new_state = mock.Mock()
    new_state.on_start = mock.Mock()
    machine.change_state(new_state)
    assert machine.cur_state == new_state
    new_state.on_start.assert_called()

