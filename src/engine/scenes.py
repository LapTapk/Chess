from vector2 import *
import game_object
from scene_utils import *
from grid import Grid


def create_start_scene():
    scene = game_object.Scene()
    bkg = create_mono_bkg(scene, (255, 255, 255))

    def change_scene():
        game.cur_scene = create_chess_scene(True)

    button = create_start_button(scene, change_scene)

    scene.init(bkg, button)
    return scene


def create_chess_scene(white_user):
    scene = game_object.Scene()
    board = create_board(scene, white_user)

    grd = board.get_component(Grid)
    grabber = create_figure_grabber(scene, grd, board,
                                    type('', (object,), {"valid": lambda x, y: True}))


    scene.init(board, grabber)
    return scene
