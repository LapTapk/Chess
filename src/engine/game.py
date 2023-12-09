import json
import pygame

DATA_JSON_PATH = 'game_data.json'

screen = None
clock = None
is_running = False
screen_size = None
fps = None
cur_scene = None
is_init = False
data = None
events = None


def init(scr_size, fps_in):
    global screen, clock, running, is_init
    global fps, cur_scene, screen_size
    global data

    if is_init:
        raise Exception("Game is already initialized")

    pygame.init()
    screen = pygame.display.set_mode(scr_size)
    clock = pygame.time.Clock()

    running = False
    screen_size = scr_size
    fps = fps_in
    cur_scene = None

    is_init = True

    with open(DATA_JSON_PATH) as f:
        data = json.load(f)


def run():
    global running
    if not is_init:
        raise Exception('Game is not initialized')

    running = True

    while running:
        __iteration()


def check_for_exit():
    global running

    for event in events:
        if event.type == pygame.QUIT:
            running = False


def __iteration():
    global events
    events = pygame.event.get()

    check_for_exit()

    screen.fill((0, 0, 0))

    cur_scene.update()

    pygame.display.update()
    clock.tick(fps)
