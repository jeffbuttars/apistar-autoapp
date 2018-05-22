from apistar import Route

from apistar_autoapp.autoapp import process_app_routes


def test_process_app_fake_routes():
    app_paths = [
        ('tests',),
        ('tests', 'v1'),
        ('tests', 'v1', 'epone'),
        ('tests', 'v1', 'eptwo'),
        ('tests', 'v1', 'epthree'),
        ('tests', 'v1', 'deep'),
        ('tests', 'v2', 'epone'),
        ('tests', 'v2', 'eptwo'),
        ('tests', 'v2', 'epthree'),
    ]

    for app_path in app_paths:
        app = {
            'app_path': app_path
        }

        res = process_app_routes(app)
        assert res
        assert not res.get('routes')

        app = {
            'routes': []
        }

        res = process_app_routes(app)
        assert res
        assert not res.get('app_path')

        app = {
            'app_path': app_path,
            'routes': [Route('/', 'GET', handler=lambda x: x)]
        }

        res = process_app_routes(app)
        assert len(res['routes']) == 1

        inc = res['routes'][0]
        assert inc.url == ('/' + '/'.join(app_path))
        assert inc.name == (':'.join(app_path))
        assert len(inc.routes) == 1

        r = inc.routes[0]
        assert r.method == 'GET'
        assert r.url =='/'


def test_process_app_real_routes():
    print('XXX test_process_app_real_routes XXX NEEDS IMPLIMENTATION')
    assert True
