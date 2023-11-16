import pygame
import renderer
import grab
from game_object import *
from vector2 import Vector2


def create_main_scene(screen):
    penguin_img = pygame.image.load('assets/character').convert_alpha()

    penguin_rend = renderer.Renderer(screen, penguin_img)
    penguin_grab = grab.Grabable()
    penguin_comps = [penguin_rend, penguin_grab]
    penguin = GameObject(Vector2(100, 300), components=penguin_comps)

    return Scene([penguin])
