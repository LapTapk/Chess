import pygame
import renderer
import grab
from game_object import *
from vector2 import Vector2


def create_test_scene():
    penguin_img = pygame.image.load('assets/character.png').convert_alpha()

    penguin_rend = renderer.Renderer(penguin_img)
    penguin_grab = grab.Grabable()
    penguin_comps = [penguin_rend, penguin_grab]
    penguin = GameObject(Vector2(100, 300), scale=Vector2(0.5, 0.5), components=penguin_comps)

    return Scene([penguin])
