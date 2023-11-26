import pygame
import game
import renderer
from grab import *
from game_object import *
from vector2 import Vector2
from grid import *

def load_image(path):
    return pygame.image.load(path).convert_alpha()


def create_grab_input_handler(grabber):
    def grab_input_handler(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            grabber.next_move()
    return grab_input_handler


def create_test_scene():
    penguin_img = load_image(game.game_data['character'])

    penguin_rend = renderer.Renderer(penguin_img)
    penguin_grab = Grabable()
    penguin_comps = [penguin_rend, penguin_grab]
    penguin = GameObject(Vector2(100, 300), scale=Vector2(
        0.5, 0.5), components=penguin_comps)

    scene = Scene([penguin])

    grabber = Grabber(scene)
    inputs = {create_grab_input_handler(grabber)}

    scene.inputs = inputs

    return scene

def __create_plane(is_light, scale):
    img = None
    name = ('light' if is_light else 'black') + '-plane'
    img = load_image(game.game_data[name])

    rend = Renderer(img)
    return GameObject(scale=Vector2(scale, scale), components=[rend])
     

def __create_board():
    plane_scale = 1.2
    plane_width = load_image(game.game_data['light-plane']).get_size()[0]
    plane_size = Vector2(plane_scale, plane_scale) * plane_width
    board_side = 8
    size = plane_size * board_side

    grid = Grid(size, Vector2(board_side, board_side))

    planes = []
    for i in range(8):
        for j in range(8):
            is_light = (i + j) % 2
            plane = __create_plane(is_light, plane_scale)
            plane_bind = GridBind(grid, Vector2(i, j))
            plane.add_component(plane_bind)
            planes.append(plane)

    offset = Vector2(0, 0)
    offset.x = offset.y = game.screen.get_size()[0] / 10
    board = GameObject(pos=offset, components=[grid]) 
    return [board] + planes


def create_chess_scene():
    return Scene(objects=__create_board()) 