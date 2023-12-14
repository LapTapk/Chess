from . import game_object
from .grid import Grid
from .scene_utils import *
from . import input_box
from .board import BoardUpdater


def create_start_scene():
    scene = game_object.Scene()
    bkg = create_mono_bkg(scene, (255, 255, 255))
    inpb_go = create_input_box(scene, 32, 'Input host IP for connection')
    inpb = inpb_go.get_component(input_box.InputBox)

    con_button = create_connect_button(scene, inpb)
    host_button = create_host_button(scene, con_button)
    con_checker = create_con_checker(scene)


    scene.init(bkg, con_button, host_button, inpb_go, con_checker)
    return scene


def create_chess_scene():
    scene = game_object.Scene()

    planes = create_planes(scene)
    grd = planes.get_component(Grid)
    board = create_board(scene, grd)

    grd = board.get_component(Grid)
    machine = create_chess_state_machine(
        scene, grd, board.get_component(BoardUpdater))

    scene.init(planes, board, machine)
    return scene
