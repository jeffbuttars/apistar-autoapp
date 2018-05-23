from apistar_autoapp.autoapp import app_args


def test_app_args_empty():
    res = app_args()

    assert res
    assert res.get('components') == []
    assert res.get('event_hooks') == []
    assert res.get('routes') == []


def test_app_args_print():
    # Make sure it doesn't explode
    res = app_args(print_results=True)
    assert res
