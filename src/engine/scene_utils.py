import pygame
import board
import game
import game_object
import renderer
import grab
import button
import grid
from board import *
from vector2 import *


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


def create_figure(scene, grd, coord, color, name):
    go = game_object.GameObject()
    rend = renderer.Renderer()
    grabable = grab.Grabable()
    binder = grid.GridBinder()

    img = load_image(game.data[color][name])
    rend.init(go, img)
    grabable.init(go, False)
    binder.init(go, grd, coord)
    go.init(scene, components=[rend, grabable, binder])
    return go


def create_figures(scene, grd, white_user):
    tfigures = [Pawn, Knight, Rook, Bishop, Queen, King]

    user_color = 'white' if white_user else 'black'
    enemy_color = 'black' if white_user else 'white'

    figures = []
    for tfigure in tfigures:
        for pos in tfigure.user_poses:
            user_figure = create_figure(scene, grd, pos,
                                         user_color, tfigure.name)
            figures.append(user_figure)

        for pos in tfigure.enemy_poses:
            enemy_figure = create_figure(scene, grd, pos,
                                          enemy_color, tfigure.name)
            figures.append(enemy_figure)

    return figures


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


def create_board(scene, white_user):
    go = game_object.GameObject()
    grd = grid.Grid()
    brd = board.Board()

    board_side = 8

    planes = []
    for i in range(board_side):
        for j in range(board_side):
            is_light = (i + j) % 2
            plane = create_plane(scene, is_light, grd,
                                 Vector2(i, j))
            planes.append(plane)

    plane_size = __calc_plane_size()
    grd.init(go, plane_size * board_side, Vector2(1, 1) * board_side)
    figures = create_figures(scene, grd, white_user)
    brd.init(go, figures)

    go.init(scene, pos=plane_size, components=[grd, brd], children=planes+figures)
    return go


def create_figure_grabber(scene, grd, board_go, board_logic):
    go = game_object.GameObject()
    grabber = grab.FigureGrabber()

    brd = board_go.get_component(Board)

    grabber.init(go, grd, brd, board_logic)
    go.init(scene, components=[grabber])
    return go


