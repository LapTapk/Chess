from . import game_object
from .grid import Grid
from .scene_utils import *
from . import input_box
from .board import BoardUpdater


def create_settings_scene():
    scene = game_object.Scene()
    bkg = create_mono_bkg(scene, pygame.color.THECOLORS['white'])

    resolution_ib = create_resolution_input_box(scene)
    apply_btn = create_apply_button(
        scene, resolution_ib.get_component(input_box.InputBox))

    start_menu_btn = create_start_menu_button(scene, create_start_scene)

    scene.init(bkg, resolution_ib, apply_btn, start_menu_btn)
    return scene


def create_start_scene():
    scene = game_object.Scene()
    bkg = create_mono_bkg(scene, pygame.color.THECOLORS['white'])
    inpb_go = create_input_box(
        scene, 32, 'Input host IP for connection', lambda x: x.isdigit() or x == '.')
    inpb = inpb_go.get_component(input_box.InputBox)

    con_button = create_connect_button(scene, inpb)
    host_button = create_host_button(scene, con_button, inpb_go)
    con_checker = create_con_checker(scene)

    setting_button = create_settings_button(scene, create_settings_scene)

    scene.init(bkg, setting_button, con_button,
               host_button, inpb_go, con_checker)
    return scene


def create_chess_scene():
    scene = game_object.Scene()

    planes = create_planes(scene)
    grd = planes.get_component(Grid)
    board = create_board(scene, grd)

    grd = board.get_component(Grid)
    machine = create_chess_state_machine(
        scene, grd, board.get_component(BoardUpdater))

    msg_comm = create_msg_comm(scene, machine.get_component(ChessStateMachine))

    bkg = create_mono_bkg(scene, pygame.color.THECOLORS['white'])
    hint = create_hint(scene)

    scene.init(bkg, planes, board, machine, msg_comm, hint)
    return scene
