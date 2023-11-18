import pygame
import renderer
from grab import *
from game_object import *
from vector2 import Vector2


def create_grab_input_handler(grabber):
    def grab_input_handler(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            grabber.next_move()
    return grab_input_handler


def create_test_scene():
    penguin_img = pygame.image.load('assets/character.png').convert_alpha()

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
