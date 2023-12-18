from src.engine.vector2 import *


def test_eq():
    v1 = Vector2(5, 6)
    v2 = Vector2(5, 6)
    assert v1 == v2


def test_add():
    v1 = Vector2(10, 7)
    v2 = Vector2(5, 40)
    v3 = v1 + v2
    assert v3 == Vector2(15, 47)


def test_sub():
    v1 = Vector2(10, 7)
    v2 = Vector2(5, 40)
    v3 = v1 - v2
    return v3 == Vector2(5, -33)

def test_mul():
    v = Vector2(35, 15)
    n = 4
    assert v * n == Vector2(140, 60)

def test_trudiv():
    v = Vector2(35, 15)
    n = 7
    assert v / n == Vector2(5, 2.142857142857143)

def test_neg():
    v = Vector2(135, 8)
    assert -v == Vector2(-135, -8)

def test_str():
    v = Vector2(16, 123)
    assert str(v) == "Vector2(16, 123)"

def test_length():
    v = Vector2(102, 37)
    right = 108.50345616615168
    assert v.length() == right

def test_to_tuple():
    v = Vector2(12, 4)
    assert v.to_tuple() == (12, 4)

def test_from_tuple():
    t = (115, 17)
    assert from_tuple(t) == Vector2(115, 17)