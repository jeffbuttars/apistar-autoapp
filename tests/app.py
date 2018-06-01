from apistar import App, ASyncApp

from apistar_autoapp import AutoApp, AutoASyncApp


# Adds coverage for the 'Using from a file named app.py' scenario, which
# is typical
def test_from_app_file():
    app = AutoApp()
    assert isinstance(app, App)
    assert app.event_hooks == []

    app = AutoASyncApp()
    assert isinstance(app, ASyncApp)
    assert app.event_hooks == []
