import os

from apistar_autoapp.autoapp import list_apps

cur_dir = os.path.realpath(os.path.dirname(__file__))


def test_list_apps_top():
    res = list_apps(cur_dir)
    assert res
    assert set(res) == set(('v1', 'v2'))


def test_list_apps_v1():
    res = list_apps(os.path.join(cur_dir, 'v1'))
    assert res
    assert set(res) == set(('epone', 'eptwo', 'epthree', 'deep'))


def test_list_apps_v2():
    res = list_apps(os.path.join(cur_dir, 'v2'))
    assert res
    assert set(res) == set(('epone', 'eptwo', 'epthree'))


def test_list_apps_v1_deep():
    res = list_apps(os.path.join(cur_dir, 'v1', 'deep'))
    assert res
    assert set(res) == set(('one', 'two'))
