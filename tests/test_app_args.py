from apistar_autoapp.autoapp import app_args
from .tools import cur_dir


def test_app_args_empty():
    res = app_args(cur_dir())

    assert res
    assert res.get('components') == []
    assert res.get('event_hooks') == []
    assert res.get('routes') == []


def test_app_args_print():
    # Make sure it doesn't explode
    res = app_args(cur_dir(), print_results=True)
    assert res
