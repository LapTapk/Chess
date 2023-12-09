from . import game_object, game
from .grid import Grid
from .scene_utils import *
from chessLogic import Board


def create_start_scene():
    scene = game_object.Scene()
    bkg = create_mono_bkg(scene, (255, 255, 255))

    def change_scene():
        game.cur_scene = create_chess_scene(True)

    button = create_start_button(scene, change_scene)

    scene.init(bkg, button)
    return scene


def create_chess_scene(is_white):
    scene = game_object.Scene()

    planes = create_planes(scene)
    grd = planes.get_component(Grid)
    board = create_board(scene, grd)

    grd = board.get_component(Grid)
    board_logic = Board.Board()
    machine = create_chess_state_machine(
        scene, grd, board, board_logic, is_white)

    scene.init(planes, board, machine)
    return scene
