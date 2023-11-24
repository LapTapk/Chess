import pygame
import input

screen = None
clock = None
is_running = False
screen_size = None
fps = None
__cur_scene = None
is_init = False


def __exit_input_handler(event):
    if event.type == pygame.QUIT:
        global running
        running = False


def init(scr_size, fps_in):
    if is_init:
        raise Exception("Game is already initialized")
    global screen, clock, running, is_init
    global fps, __cur_scene, screen_size

    pygame.init()
    screen = pygame.display.set_mode(scr_size)
    clock = pygame.time.Clock()

    running = False
    screen_size = scr_size
    fps = fps_in
    __cur_scene = None

    input.input_handlers |= {__exit_input_handler}

    is_init = True


def get_cur_scene():
    return __cur_scene


def set_cur_scene(new_scene):
    global __cur_scene

    if __cur_scene != None:
        input.input_handlers -= __cur_scene.inputs

    __cur_scene = new_scene
    input.input_handlers |= new_scene.inputs


def run():
    global running
    if not is_init:
        raise Exception('Game is not initialized')

    running = True

    while running:
        __iteration()


def __iteration():
    input.handle_inputs()

    screen.fill((0, 0, 0))

    __cur_scene.update()

    pygame.display.update()
    clock.tick(fps)
