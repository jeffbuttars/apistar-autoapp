#  import pytest
from apistar import App, ASyncApp
from apistar_autoapp import AutoApp, AutoASyncApp


def test_empty_autoApp():
    app = AutoApp()
    assert isinstance(app, App)


def test_empty_autoASyncApp():
    app = AutoASyncApp()
    assert isinstance(app, ASyncApp)
