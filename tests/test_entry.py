from apistar import App, ASyncApp

from apistar_autoapp import AutoApp, AutoASyncApp

from .app import test_from_app_file


def test_empty_autoApp():
    app = AutoApp()
    assert isinstance(app, App)
    assert app.event_hooks == []


def test_empty_autoASyncApp():
    app = AutoASyncApp()
    assert isinstance(app, ASyncApp)
    assert app.event_hooks == []


def test_app_entry():
    test_from_app_file()
