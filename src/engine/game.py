import pygame


class Game:
    instance = None

    def __init__(self, screen_size, fps):
        if Game.instance != None:
            raise Exception(
                "More than one instance of Game is initialized (must be singleton)")

        Game.instance = self

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()

        self.running = False
        self.screen_size = screen_size
        self.fps = fps
        self.cur_scene = None

    def run(self):
        self.running = True


        #self.screen = pygame.display.set_mode(self.screen_size)
        #self.clock = pygame.time.Clock()

        while self.running:
            self.iteration()

    def iteration(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill((0, 0, 0))

        self.cur_scene.update()

        pygame.display.update()
        self.clock.tick(self.fps)
