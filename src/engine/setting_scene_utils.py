'''Не предназначено для использования, сугубо вспомогательный в создании сцен модуль.'''

from . import game


def try_apply_resolution(resolution_ib):
    try:
        reso = tuple(map(int, resolution_ib.text.split()))
        game.change_screen_size(reso)
    except:
        pass


def apply(resolution_ib):
    try_apply_resolution(resolution_ib)
