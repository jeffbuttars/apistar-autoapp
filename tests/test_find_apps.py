import os
import inspect
from apistar_autoapp.autoapp import find_apps


def cur_dir():
    frame = inspect.stack()[0]
    module = inspect.getmodule(frame[0])
    return os.path.dirname(os.path.realpath(module.__file__))


def test_find_apps_top():
    res = find_apps(cur_dir())
    assert res
    assert set(res) == set(('v1', 'v2'))


def test_find_apps_v1():
    res = find_apps(os.path.join(cur_dir(), 'v1'))
    assert res
    assert set(res) == set(('epone', 'eptwo', 'epthree', 'deep'))


def test_find_apps_v2():
    res = find_apps(os.path.join(cur_dir(), 'v2'))
    assert res
    assert set(res) == set(('epone', 'eptwo', 'epthree'))


def test_find_apps_v1_deep():
    res = find_apps(os.path.join(cur_dir(), 'v1', 'deep'))
    assert res
    assert set(res) == set(('one', 'two'))
