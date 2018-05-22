import pytest
from apistar_autoapp.autoapp import inspect_app


def test_inspect_app_top():
    with pytest.raises(TypeError):
        inspect_app()

    with pytest.raises(ModuleNotFoundError):
        inspect_app(tuple())

    res = inspect_app(('tests',))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests',)


def test_inspect_app_v1():
    res = inspect_app(('tests', 'v1'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v1')


def test_inspect_app_v2():
    res = inspect_app(('tests', 'v2'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v2')

def test_inspect_app_v1_subs():
    res = inspect_app(('tests', 'v1', 'epone'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v1', 'epone')

    res = inspect_app(('tests', 'v1', 'eptwo'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v1', 'eptwo')

    res = inspect_app(('tests', 'v1', 'epthree'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v1', 'epthree')

    res = inspect_app(('tests', 'v1', 'deep'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v1', 'deep')


def test_inspect_app_v2_subs():
    res = inspect_app(('tests', 'v2', 'epone'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v2', 'epone')

    res = inspect_app(('tests', 'v2', 'eptwo'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v2', 'eptwo')

    res = inspect_app(('tests', 'v2', 'epthree'))
    assert res
    assert res['routes'] == []
    assert res['components'] == []
    assert res['template_dir'] == []
    assert res['packages'] == []
    assert res['event_hooks'] == []
    assert res['app_path'] == ('tests', 'v2', 'epthree')

    with pytest.raises(ModuleNotFoundError):
        inspect_app(('tests', 'v2', 'empty'))
