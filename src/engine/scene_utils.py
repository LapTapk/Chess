'''Не предназначено для использования, сугубо вспомогательный в создании сцен модуль.'''

import pygame
import socket
from . import game_object, input_box, renderer, game, message_communication, \
    button, grid, board, grab, connection_checker, setting_scene_utils
from .vector2 import *
from .chess_state_machine import *
from chess_server import server, client


def load_image(path):
    return pygame.image.load(path).convert_alpha()


def create_mono_bkg(scene, color):
    go = game_object.GameObject()
    rend = renderer.Renderer()
    def_scr_size = game.data['default-screen-size']
    img = pygame.Surface(def_scr_size)
    pygame.draw.rect(img, color, img.get_rect())
    rend.init(go, img)

    pos = from_tuple(def_scr_size) / 2
    go.init(scene, pos=pos, components=[rend])
    return go


def create_button(scene, pos, img_name, *funcs, scale=Vector2(1, 1)):
    go = game_object.GameObject()
    rend = renderer.Renderer()
    btn = button.Button()

    img = load_image(game.data[img_name])
    rend.init(go, img)
    btn.init(go, rend, *funcs)

    go.init(scene, pos=pos, scale=scale, components=[rend, btn])
    return go


def create_connect_button(scene, inpb):
    def try_connect():
        host = inpb.text
        try:
            game.clnt = client.Client(host, 80, False)
        except Exception as e:
            print(e)
            return

    def_scr_size = game.data['default-screen-size']

    pos = from_tuple(def_scr_size) / 2 - Vector2(200, 0)
    btn_go = create_button(scene, pos, 'connect-btn', try_connect)
    return btn_go


def create_host_button(scene, connect_btn, ip_ib):
    def host():
        try: 
            if server.is_init:
                return
            address = ip_ib.text
            server.init((address, 80))

            game.clnt = client.Client(address, 80, True)
            connect_btn.enabled = False
            ip_ib.enabled = False
        except Exception as e:
            print(e)

    if server.is_init:
        connect_btn.enabled = False

    def_scr_size = game.data['default-screen-size']
    pos = from_tuple(def_scr_size) / 2 + Vector2(200, 0)
    btn_go = create_button(scene, pos, 'host-btn', host)

    return btn_go


def create_plane(scene, is_light, grd, coord):
    go = game_object.GameObject()
    rend = renderer.Renderer()
    binder = grid.GridBinder()

    color = 'light' if is_light else 'black'
    img = load_image(game.data[f'{color}-plane'])
    rend.init(go, img)
    binder.init(go, grd, coord)
    go.init(scene, components=[binder, rend])
    return go


def __calc_plane_size():
    dummy_plane = create_plane(None, True, grid.Grid(), (0, 0))
    plane_rect = dummy_plane.get_component(renderer.Renderer).get_rect()
    plane_size = Vector2(plane_rect.w, plane_rect.h)
    return plane_size


def create_planes(scene):
    go = game_object.GameObject()
    grd = grid.Grid()

    board_side = 8
    plane_size = __calc_plane_size()
    grd_size = plane_size * board_side - plane_size
    grd.init(go, grd_size, Vector2(1, 1) * board_side)
    planes = []
    for i in range(board_side):
        for j in range(board_side):
            is_light = (i + j + 1) % 2
            plane = create_plane(scene, is_light, grd,
                                 Vector2(i, j))
            planes.append(plane)
    go.init(scene, pos=plane_size, components=[grd], children=planes)
    return go


def create_board(scene, grd):
    go = game_object.GameObject()
    brd = board.BoardUpdater()

    brd.init(go, grd)

    go.init(scene, components=[grd, brd])
    return go


def create_figure_grabber(go, grd):
    grabber = grab.FigureGrabber()
    grabber.init(go, grd)
    return grabber


def create_chess_state_machine(scene, grd, brd):
    go = game_object.GameObject()
    machine = ChessStateMachine()
    grabber = create_figure_grabber(go, grd)

    machine.init(go, grabber, brd)
    go.init(scene, components=[machine])
    return go


def create_input_box(scene, font_size, invitation, is_valid):
    go = game_object.GameObject()
    rend = renderer.Renderer()
    inpb = input_box.InputBox()

    rend.init(go, pygame.surface.Surface((0, 0)))
    inpb.init(go, font_size, invitation, is_valid, rend)

    def_scr_size = game.data['default-screen-size']
    pos = from_tuple(def_scr_size) / 2 + Vector2(0, 200)
    go.init(scene, pos=pos, components=[inpb, rend])
    return go


def create_con_checker(scene):
    go = game_object.GameObject()
    con_checker = connection_checker.ConnectionChecker()

    go.init(scene, components=[con_checker])
    return go


def create_change_scene_button(scene, pos, img_name, create_scene):
    def change_scene():
        game.cur_scene = create_scene()

    return create_button(scene, pos, img_name, change_scene, scale=Vector2(1/2, 1/2))


def create_settings_button(scene, create_scene):
    pos = from_tuple(game.data['default-screen-size']) - Vector2(100, 50)
    return create_change_scene_button(scene, pos, 'settings-btn', create_scene)


def create_start_menu_button(scene, create_scene):
    pos = from_tuple(game.data['default-screen-size']) - Vector2(100, 50)
    return create_change_scene_button(scene, pos, 'play-button', create_scene)


def create_resolution_input_box(scene):
    go = game_object.GameObject()
    ib = input_box.InputBox()
    rend = renderer.Renderer()

    rend.init(go, pygame.surface.Surface((0, 0)))
    ib.init(go, 32, 'Input screen size',
            lambda x: x.isdigit() or x == ' ', rend)
    go.init(scene, pos=Vector2(640, 100), components=[ib, rend])
    return go


def create_apply_button(scene, resolution_ib):
    def apply():
        setting_scene_utils.apply(resolution_ib)

    return create_button(scene, Vector2(640, 600), 'apply-btn', apply)


def create_msg_comm(scene, chess_state_machine):
    go = game_object.GameObject()
    rend = renderer.Renderer()
    msg_comm = message_communication.MessageCommunication()

    rend.init(go, pygame.surface.Surface((0, 0)))
    msg_comm.init(go, 24, chess_state_machine, rend)
    pos = Vector2(900, 200)
    go.init(scene, pos=pos, components=[msg_comm, rend])
    return go


def create_hint(scene):
    go = game_object.GameObject()
    rend = renderer.Renderer()
    text = 's - сдаться/ок || d- ничья?/нет'
    font = pygame.font.Font(None, 32)

    rend.init(go, font.render(text, False, (0, 0, 0)))
    pos = Vector2(900, 400)
    go.init(scene, pos=pos, components=[rend])
    return go
