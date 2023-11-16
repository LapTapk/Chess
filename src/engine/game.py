import pygame


class Game:
    def __init__(self, screen_size, fps, first_scene):
        self.running = False
        self.screen_size = screen_size
        self.fps = fps
        self.cur_scene = first_scene

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode(self.screen_size)
        clock = pygame.time.Clock()

        while self.running:
            self.iteration(screen, clock)

    def iteration(self, screen, clock):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        screen.fill(0, 0, 0)
        self.cur_scene.update()
        clock.tick(self.data.fps)
