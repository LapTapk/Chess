from . import game_object
from .grid import Grid
from .scene_utils import *
from . import input_box


def create_start_scene():
    scene = game_object.Scene()
    bkg = create_mono_bkg(scene, (255, 255, 255))
    inpb_go = create_input_box(scene, 32, 'Input host ip')
    inpb = inpb_go.get_component(input_box.InputBox)

    con_button = create_connect_button(scene, inpb, create_chess_scene)
    host_button = create_host_button(scene, create_chess_scene, con_button)

    scene.init(bkg, con_button, host_button, inpb_go)
    return scene


def create_chess_scene():
    scene = game_object.Scene()

    planes = create_planes(scene)
    grd = planes.get_component(Grid)
    board = create_board(scene, grd)

    grd = board.get_component(Grid)
    machine = create_chess_state_machine(
        scene, grd, board, game.client.is_white)

    scene.init(planes, board, machine)
    return scene
