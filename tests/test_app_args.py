from apistar_autoapp.autoapp import app_args
from .tools import cur_dir


def test_app_args_empty():
    res = app_args(cur_dir())

    print('test_app_args', res)
    assert res
    assert res.get('components') == []
    assert res.get('event_hooks') == []
    assert res.get('routes') == []
