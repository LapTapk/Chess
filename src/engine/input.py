import pygame


input_handlers = set()


def handle_inputs():
    for event in pygame.event.get():
        for h in input_handlers:
            h(event)
