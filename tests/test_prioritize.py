from apistar_autoapp import autoapp

app1 = {
    'app_path': ('v1',)
}
app2 = {
    'app_path': ('v1', 'l1')
}
app3 = {
    'app_path': ('v1', 'l2')
}
app4 = {
    'app_path': ('v1', 'l2', 'll1')
}

apps = [
    app1, app2, app3, app4
]


def app_path(app):
    return '.'.join(app.get('app_path'))


def test_prioritize_none():
    res = autoapp.prioritize([], apps)
    assert res
    assert res == apps


def test_prioritize_some():
    res = autoapp.prioritize(
        [app_path(app4), app_path(app2)],
        apps
    )

    assert res
    assert res == [app4, app2, app1, app3]


def test_prioritize_reverse():
    res = autoapp.prioritize(
        [app_path(app4), app_path(app3), app_path(app2), app_path(app1)],
        apps
    )
    assert res
    assert res == [app4, app3, app2, app1]


def test_prioritize_all():
    res = autoapp.prioritize(
        [app_path(app4), app_path(app2), app_path(app3), app_path(app1)],
        apps
    )
    assert res
    assert res == [app4, app2, app3, app1]
