import pygame
from . import game_object, renderer, game, \
    button, grid, board, grab 
from .vector2 import *
from .board import BoardUpdater
from .chess_state_machine import *

def load_image(path):
    return pygame.image.load(path).convert_alpha()


def create_mono_bkg(scene, color):
    go = game_object.GameObject()
    rend = renderer.Renderer()

    img = pygame.Surface(game.screen_size)
    pygame.draw.rect(img, color, img.get_rect())
    rend.init(go, img)

    pos = from_tuple(game.screen_size) / 2
    go.init(scene, pos=pos, components=[rend])
    return go


def create_start_button(scene, *funcs):
    go = game_object.GameObject()
    rend = renderer.Renderer()
    btn = button.Button()

    img = load_image(game.data['play-button'])
    rend.init(go, img)
    btn.init(go, rend, *funcs)

    pos = from_tuple(game.screen_size) / 2
    go.init(scene, pos=pos, components=[rend, btn])
    return go



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
    grd.init(go, plane_size * board_side, Vector2(1, 1) * board_side)
    planes = []
    for i in range(board_side):
        for j in range(board_side):
            is_light = (i + j) % 2
            plane = create_plane(scene, is_light, grd,
                                 Vector2(i, j))
            planes.append(plane)
    go.init(scene, pos=plane_size, children=planes)
    return go


def create_board(scene, grd):
    go = game_object.GameObject()
    brd = board.BoardUpdater()

    brd.init(go, grd)

    go.init(scene, components=[grd, brd])
    return go


def create_figure_grabber(go, grd, board_go, board_logic):
    grabber = grab.FigureGrabber()
    brd = board_go.get_component(BoardUpdater)
    grabber.init(go, grd, brd, board_logic)
    return grabber

def create_chess_state_machine(scene, grd, brd, board_logic, is_white):
    go = game_object.GameObject()
    machine = ChessStateMachine()
    user_turn_state = UserTurnState()
    grabber = create_figure_grabber(go, grd, brd, board_logic)

    user_turn_state.init(machine, grabber, board_logic, is_white)
    machine.init(go, user_turn_state)
    go.init(scene, components=[machine])
    return go
    