import game
from renderer import Renderer
from vector2 import Vector2


class GameObject:
    def init(self, scene, pos=Vector2(0, 0), rot=0, scale=Vector2(1, 1), components=[]):
        self.position = pos
        self.rotation = rot
        factor_x = game.screen_size[0] / \
            game.game_data['default-screen-size'][0]
        factor_y = game.screen_size[1] / \
            game.game_data['default-screen-size'][1]
        self.scale = Vector2(scale.x * factor_x, scale.y * factor_y)

        self.components = components
        self.scene = scene

    def get_component(self, type):
        for comp in self.components:
            if isinstance(comp, type):
                return comp

        return None

    def add_component(self, comp):
        self.components.append(comp)
        comp.go = self


class Scene:
    def init(self, objects):
        self.objects = objects

    def update(self):
        for obj in self.objects:
            for comp in obj.components:
                comp.update()

    def at_point(self, point):
        res = []
        for obj in self.objects:
            rend = obj.get_component(Renderer)
            if rend == None:
                continue
            rect = rend.get_rect()
            if rect.collidepoint(point):
                res.append(obj)

        return res

    def add_object(self, go):
        self.objects.append(go)
        go.scene = self
