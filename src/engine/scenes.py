import pygame
import game
import renderer
from grab import *
from game_object import *
from vector2 import Vector2
from grid import *

def __load_image(path):
    return pygame.image.load(path).convert_alpha()


def __create_figure_grab_input_handler(grabber):
    def grab_input_handler(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if grabber.grabber.grabbed == None:
                grabber.try_grab()
            else:
                grabber.drop()
    return grab_input_handler

def __create_grab_input_handler(grabber):
    def grab_input_handler(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if grabber.grabbed == None:
                grabber.try_grab()
            else:
                grabber.drop()
    return grab_input_handler


def create_test_scene():
    penguin_img = __load_image(game.game_data['character'])

    penguin_rend = renderer.Renderer(penguin_img)
    penguin_grab = Grabable()
    penguin_comps = [penguin_rend, penguin_grab]
    penguin = GameObject(Vector2(100, 300), scale=Vector2(
        0.5, 0.5), components=penguin_comps)

    scene = Scene([penguin])

    grabber = Grabber(scene)
    inputs = {__create_grab_input_handler(grabber)}

    scene.inputs = inputs

    return scene

def __create_plane(is_light, scale):
    img = None
    name = ('light' if is_light else 'black') + '-plane'
    img = __load_image(game.game_data[name])

    rend = Renderer(img)
    return GameObject(scale=Vector2(scale, scale), components=[rend])
     

def __create_board():
    dummy_plane = __create_plane(True, 1.2)
    plane_rect = dummy_plane.get_component(Renderer).get_rect()
    plane_size = Vector2(plane_rect.w, plane_rect.h)

    board_side = 8
    grid_size = plane_size * board_side

    grid = Grid(grid_size, Vector2(board_side, board_side))

    planes = []
    for i in range(8):
        for j in range(8):
            is_light = (i + j) % 2
            plane = __create_plane(is_light, 1.2)
            plane_bind = GridBind(grid, Vector2(i, j))
            plane.add_component(plane_bind)
            planes.append(plane)

    offset = Vector2(0, 0)
    offset.x = offset.y = game.screen.get_size()[0] / 10
    board = GameObject(pos=offset, components=[grid]) 
    return [board] + planes


def __create_test_figure(grid, scale):
    img = __load_image(game.game_data['character'])

    rend = Renderer(img)
    binder = GridBind(grid, Vector2(0, 0))
    grabable = Grabable()

    comps = [binder, rend, grabable]
    go = GameObject(scale=Vector2(scale, scale), components=comps)
    return go


def create_chess_scene():
    board = __create_board()
    scene = Scene(board) 

    board_grid = board[0].get_component(Grid)
    grab = FigureGrab(scene, board_grid, Grabber(scene))
    scene.inputs = {__create_figure_grab_input_handler(grab)}

    figure = __create_test_figure(board_grid, 1/4)

    scene.add_object(figure)

    return scene
