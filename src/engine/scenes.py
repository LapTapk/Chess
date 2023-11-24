import pygame
import game
import renderer
import json
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
    penguin_img = load_image('assets/character.png')

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

def __create_plane(is_light):
    img = None
    name = ('light' if is_light else 'black') + '-plane'
    img = load_image(game.game_data[name])

    rend = Renderer(img)
    return GameObject(components=[rend])
     

def __create_board():
    screen_size = game.screen.get_size()
    size = Vector2(0, 0)
    size.x = size.y = screen_size[1] * game.game_data['board-screen-ratio']

    grid = Grid(size, Vector2(8, 8))
    planes = []
    for i in range(8):
        for j in range(8):
            is_light = (i + j) % 2
            plane = __create_plane(is_light)
            plane_bind = GridBind(grid, Vector2(i, j))
            plane.add_component(plane_bind)
            planes.append(plane)

    offset = Vector2(0, 0)
    offset.x = offset.y = game.screen.get_size()[0] - size.x
    board = GameObject(pos=offset, components=[grid]) 
    return [board] + planes


def create_chess_scene():
    return Scene(objects=__create_board()) 