from . import game
from .renderer import Renderer
from .vector2 import Vector2
from typing import *


class Scene:
    '''
    Сущность, являющаяся совокупностью всех элементарных частиц ``GameObject``.
    '''

    def init(self, *objects):
        '''
        Инициализатор. Аналогичен __init__. 
        Все параметры метода соответствуют полям класса.
        '''
        self.objects: List[GameObject] = list(objects)
        '''Список объектов, принадлежащих текущей ``Scene``'''

    def __update_obj(self, obj) -> None:
        '''
        Служебный метод, выполняющий ту же функцию, что и *update*.

        :param obj: ``GameObject``, у которого нужно вызвать update.
        :type obj: GameObject
        '''
        if not obj.enabled:
            return

        for comp in obj.components:
            comp.update()

        for c_obj in obj.children:
            self.__update_obj(c_obj)

    def update(self) -> None:
        '''
        Метод, вызывающий метод update 
        для каждого компонента каждого объекта данной ``Scene``.
        '''
        for obj in self.objects:
            self.__update_obj(obj)

    def __at_point_rec(self, obj, point: Tuple[int, int]) -> List[Any]:
        '''
        Служебный метод, выполняющий ту же функцию, что и *at_point*.

        :param obj: ``GameObject``, для которого необходимо выполнить проверку на пересечение с точкой *point*.
        :type obj: GameObject
        :param point: точка, в которой осуществляется поиск ``GameObject``.
        :return: список ``GameObject``, располагающихся под заданной точкой.
        '''
        res = []

        rend = obj.get_component(Renderer)
        if rend != None:
            rect = rend.get_rect()
            if rect.collidepoint(point):
                res.append(obj)

        for child in obj.children:
            res.extend(self.__at_point_rec(child, point))

        return res

    def at_point(self, point: Tuple[int, int]) -> List[Any]:
        '''
        Метод, находящий все ``GameObject``, которые пересекают данную точку
        рисунком ``Renderer``.
        :return: список ``GameObject``, располагающихся под заданной точкой.
        '''
        res = []
        for obj in self.objects:
            res.extend(self.__at_point_rec(obj, point))

        return res

    def add_object(self, go) -> None:
        '''
        Метод, добавляющий ``GameObject`` в ``Scene``.
         
        :param go: добавляемый ``GameObject``.
        :type go: GameObject
        '''
        self.objects.append(go)
        go.scene = self


class GameObject:
    '''
    Элементарная сущность, хранящая характеристики и поведение,
    согласно которому она должна действовать на сцене.
    '''

    def init(self, scene: Scene, pos=Vector2(0, 0), rot=0, scale=Vector2(1, 1), components=[], children=[]) -> None:
        '''
        Инициализатор. Аналогична __init__. Каждый параметр функции
        соотносится с параметром класса.
        '''
        self.rotation: int = rot
        '''Угол поворота ``GameObject`` в градусах.'''

        factor_x = game.screen_size[0] / \
            game.data['default-screen-size'][0]
        factor_y = game.screen_size[1] / \
            game.data['default-screen-size'][1]
        self.scale: Vector2 = Vector2(scale.x * factor_x, scale.y * factor_y)
        '''Коэффициент при размере ``GameObject``.'''
        self.position: Vector2 = Vector2(pos.x * factor_x, pos.y * factor_y)
        '''Расположение ``GameObject`` на сцене.'''

        self.components: List[Any] = components
        '''Компоненты, определяющие поведение ``GameObject``.'''
        self.scene: Scene = scene
        '''Cцена, в которой располагается этот ``GameObject``.'''
        self.children: List[GameObject] = children
        '''Дочерние ``GameObject``.'''
        self.enabled: bool = True
        '''Принимает ли участие данный ``GameObject`` в сцене'''

    def get_component(self, type: Any) -> type:
        '''
        Метод, возвращающий компонент определенного типа 
        из компонентов данного ``GameObject``.

        :param type: тип искомого компонента.
        :return: компонент данного типа.
        '''
        for comp in self.components:
            if isinstance(comp, type):
                return comp

    def add_component(self, comp: Any) -> None:
        '''
        Процедура, добавляющая компонент в список компонентов ``GameObject``.
        '''
        self.components.append(comp)
        comp.go = self
