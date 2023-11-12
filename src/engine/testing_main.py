import pygame
from game_object import GameObject
from vector2 import *
from scene import Scene
from renderer import Renderer

pygame.init()

clock = pygame.time.Clock()

screen_size = Vector2(700, 500)
screen = pygame.display.set_mode(screen_size.to_tuple())

img = pygame.image.load('assets/character.png').convert_alpha()
rend = Renderer(screen, img)
go = GameObject(Vector2(200, 300), scale=Vector2(100, 100), components=[rend])

objs = [go]
scene = Scene(objs)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill((0, 0, 0)) 

    scene.update()
    screen.blit(img, (100, 100))

    pygame.display.update()

    clock.tick(60)
