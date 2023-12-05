import game
from renderer import Renderer
from vector2 import Vector2


class GameObject:
    def init(self, scene, pos=Vector2(0, 0), rot=0, scale=Vector2(1, 1), components=[], children=[]):
        self.position = pos
        self.rotation = rot

        factor_x = game.screen_size[0] / \
            game.game_data['default-screen-size'][0]
        factor_y = game.screen_size[1] / \
            game.game_data['default-screen-size'][1]
        self.scale = Vector2(scale.x * factor_x, scale.y * factor_y)

        self.components = components
        self.scene = scene
        self.children = children

    def get_component(self, type):
        for comp in self.components:
            if isinstance(comp, type):
                return comp

        return None

    def add_component(self, comp):
        self.components.append(comp)
        comp.go = self


class Scene:
    def init(self, *objects):
        self.objects = objects

    def __update_obj(self, obj):
        for comp in obj.components:
            comp.update()

        for c_obj in obj.children:
            self.__update_obj(c_obj)

    def update(self):
        for obj in self.objects:
            self.__update_obj(obj)

    def __at_point_rec(self, obj, point):
        res = []

        rend = obj.get_component(Renderer)
        if rend != None:
            rect = rend.get_rect()
            if rect.collidepoint(point):
                res.append(obj)

        for child in obj.children:
            res.extend(self.__at_point_rec(child, point))

        return res

    def at_point(self, point):
        res = []
        for obj in self.objects:
            res.extend(self.__at_point_rec(obj, point))

        return res

    def add_object(self, go):
        self.objects.append(go)
        go.scene = self
