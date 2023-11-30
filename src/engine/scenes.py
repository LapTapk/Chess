from button import Button
import pygame
import game
import renderer
from grab import *
from game_object import *
from vector2 import Vector2
from grid import *


def __load_image(path):
    return pygame.image.load(path).convert_alpha()


def __create_plane(scene, is_light):
    rend = Renderer()
    go = GameObject()

    img = None
    name = ('light' if is_light else 'black') + '-plane'
    img = __load_image(game.game_data[name])

    rend.init(go, img)
    scale = 1.2
    go.init(scene, scale=Vector2(scale, scale), components=[rend])

    return go


def __calc_plane_size():
    dummy_plane = __create_plane(None, True)
    plane_rect = dummy_plane.get_component(Renderer).get_rect()
    plane_size = Vector2(plane_rect.w, plane_rect.h)
    return plane_size

def __create_board(scene):
    board = GameObject()
    grid = Grid()

    plane_size = __calc_plane_size()
    board_side = 8
    grid_size = plane_size * board_side

    grid.init(board, grid_size, Vector2(board_side, board_side))

    planes = []
    for i in range(8):
        for j in range(8):
            is_light = (i + j) % 2
            plane = __create_plane(scene, is_light)

            plane_bind = GridBind()
            plane_bind.init(plane, grid, Vector2(i, j))
            plane.components.append(plane_bind)

            planes.append(plane)

    offset = Vector2(0, 0)
    offset.x = offset.y = game.screen.get_size()[0] / 10
    board.init(scene, pos=offset, components=[grid])
    return board, planes


def __create_test_figure(scene, grid):
    img = __load_image(game.game_data['character'])

    go = GameObject()
    rend = Renderer()
    binder = GridBind()
    grabable = Grabable()

    scale = 1/6
    comps = [binder, rend, grabable]
    go.init(scene, scale=Vector2(scale, scale), components=comps)
    rend.init(go, img)
    binder.init(go, grid, Vector2(0, 0))
    grabable.init(go)

    return go


def create_chess_scene():
    scene = Scene()

    board, planes = __create_board(scene)

    grabber_go = GameObject()
    grid_grabber = GridGrab()

    board_grid = board.get_component(Grid)
    figure = __create_test_figure(scene, board_grid)

    scene.init(planes + [figure, board, grabber_go])
    grabber_go.init(scene, components=[grid_grabber])
    grid_grabber.init(grabber_go, board_grid)


    return scene

def __create_start_button(scene):
    go = GameObject()
    rend = Renderer()
    button = Button()
    
    img = __load_image(game.game_data['light-plane'])

    def change_scene():
        game.cur_scene = create_chess_scene()
    
    pos = from_tuple(game.screen_size) / 2
    go.init(scene, pos=pos, components=[rend, button])
    rend.init(go, img)
    button.init(go, change_scene)
    return go


def create_start_menu_scene():
    scene = Scene()
    button = __create_start_button(scene)

    scene.init([button])
    return scene