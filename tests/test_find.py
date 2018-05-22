from apistar_autoapp import autoapp

from .tools import cur_dir


def test_find():
    res = autoapp.find(cur_dir(), ('tests',))
    assert res
    assert len(res) == 11

    #  from pprint import pformat as pf
    #  print('test_find', len(res), pf(res))

    for app in res:
        assert app.get('components') == []
        assert app.get('event_hooks') == []
        assert app.get('packages') == []
        assert app.get('routes') == []
        assert app.get('template_dir') == []
        assert app.get('app_path')
        assert len(app.get('app_path')) > 0
        assert app.get('app_path')[0] == 'tests'
