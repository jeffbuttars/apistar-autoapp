import os

from apistar_autoapp import autoapp

cur_dir = os.path.realpath(os.path.dirname(__file__))


def test_find_apps():
    res = autoapp.find_apps(cur_dir)
    assert res
    assert len(res) == 11

    for app in res:
        assert app.get('components') == []
        assert app.get('event_hooks') == []
        assert app.get('packages') == []
        assert app.get('routes') == []
        assert app.get('template_dir') == []
        assert app.get('app_path')
        assert len(app.get('app_path')) > 0
