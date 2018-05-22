import inspect
import logging
import os
from importlib import import_module

from apistar import App, ASyncApp, Include

logger = logging.getLogger('autoapp')
_tab = '  '


def print_include(include, printer: callable, level: int = 0):
    printer('{}Include: {} {}'.format(_tab * level, include.url, include.name))

    for route in include.routes:
        print_route(route, printer, parent_url=include.url, level=level + 1)


def print_route(route, printer, parent_url: str = None, level: int = 0):
    url = parent_url + route.url if parent_url else route.url

    argspec = inspect.getfullargspec(route.handler)

    # Build the return type string if it's annotated
    return_str = ''
    return_spec = argspec.annotations.get('return')
    if return_spec:
        return_str = ' -> {}:'.format(return_spec.__name__)

    # Build a dict of each args default value
    #     Pad the values of the defaults tuple to match the args list,
    #     then zip the two together to create a dict for easy lookup later
    def_vals = argspec.defaults or tuple()
    def_vals = (('',) * (len(argspec.args) - len(def_vals))) + def_vals
    arg_defs = dict(zip(argspec.args, def_vals))

    # Build a signature string from args, annotations and defaults
    args_str = ''
    for arg in argspec.args:
        spec = argspec.annotations.get(arg, '')

        spec_str = ''
        if spec:
            spec_str = ': {}'.format(spec.__name__)

        adef = arg_defs.get(arg)
        if adef:
            spec_str = '{}={}'.format(spec_str, adef)

        args_str += '{}{}, '.format(arg, spec_str)

    args_str = args_str[:-2]

    route_handler = route.handler.__module__ + '.' + route.handler.__qualname__
    route_handler = '{}.{}({}){}'.format(
        route.handler.__module__, route.handler.__qualname__, args_str, return_str
    )

    printer('{}Route: {:>3} {}, {}'.format(_tab * level, route.method, url, route.name))
    printer('{} {}'.format(_tab * (level + 3), route_handler))


def print_routes(routes, printer=None):
    printer = printer or logger.debug

    printer('\nRoutes:')

    for route in routes:
        if hasattr(route, 'routes'):
            print_include(route, printer, level=1)
        else:
            print_route(route, printer, level=1)


def print_components(components, printer=None):
    printer = printer or logger.debug

    printer('\nComponents:')
    for comp in components:
        printer('\t{}'.format(comp.__class__.__name__))


def find_apps(app_dir: str) -> list:
    """
    For a given directory, return all the 'app's in it.
    """
    apps = []

    for de in os.scandir(app_dir):
        if de.is_dir() and os.path.isfile(os.path.join(app_dir, de.name, 'app.py')):
            apps.append(de.name)

    return apps


def inspect_app(app_path: tuple) -> dict:
    """
    Return the attributes need for the App() instance from this app's app.py
    """
    path_str = '.'.join(app_path + ('app',))
    app_mod = import_module(path_str)

    return {
        'routes': getattr(app_mod, 'routes', []),
        'components': getattr(app_mod, 'components', []),
        'template_dir': getattr(app_mod, 'template_dir', []),
        'static_dir': getattr(app_mod, 'static_dir', ''),
        'packages': getattr(app_mod, 'packages', []),
        'event_hooks': getattr(app_mod, 'event_hooks', []),
        'app_path': app_path,
    }


def process_app_routes(app):
    """
    For a given dict of app data figure out if the app is nested
    and if so convert the routes to an Include with the appropriate
    URL prefix.
    """

    routes = app.get('routes')
    app_path = app.get('app_path')

    # If the app has no routes or is not nested (no or empty app_path), do nothing.
    if not routes or not app_path:
        return app

    # Build an Include for the set of nested URLs with the matching prefix
    # for the directory structure
    app['routes'] = [Include(
        '/' + '/'.join(app_path),
        name=':'.join(app_path),
        routes=routes,
    )]

    return app


def find(cur_dir: str, parent_app: tuple = None):
    res = []

    sub_apps = find_apps(cur_dir)
    parent_app = parent_app if parent_app else tuple()

    for app_name in sub_apps:
        app_path = parent_app + (app_name,)
        cur_app = inspect_app(app_path)

        # Decend into each found app
        sub_res = find(os.path.join(cur_dir, app_name), app_path)
        res += [cur_app] + sub_res

    return res


def prioritize(priority_apps, reg_apps):
    if not priority_apps:
        return reg_apps

    # Sort the reg_apps so the priority_apps are honored and first
    papps = []
    apps = reg_apps.copy()

    for papp in priority_apps:
        papp_path = tuple(papp.split('.'))

        for sapp in apps:
            if papp_path == sapp.get('app_path', tuple()):
                papps.append(sapp)
                apps.remove(sapp)

    return papps + apps


def app_args(project_dir: str = None,
             priority_apps: list = None,
             print_results: bool = False,
             **kwargs) -> dict:

    sub_routes = []
    sub_comps = []
    sub_hooks = []

    if not project_dir:
        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        project_dir = module.__file__

    # Find all the sub apps and collect their info then prioritize them
    sub_apps = prioritize(
        priority_apps,
        find(os.path.dirname(os.path.realpath(project_dir)))
    )

    # Collect and process all the sub app data
    for sapp in sub_apps:
        sapp = process_app_routes(sapp)
        sub_routes += sapp.get('routes', [])
        sub_comps += sapp.get('components', [])
        sub_hooks += sapp.get('event_hooks', [])

    # Append the sub app data into the existing app data giving precedence to the
    # existing data
    kwargs['components'] = kwargs.get('components', []) + sub_comps
    kwargs['event_hooks'] = kwargs.get('event_hooks', []) + sub_hooks
    kwargs['routes'] = kwargs.get('routes', []) + sub_routes

    if print_results:
        print_components(kwargs['components'], printer=print)
        print_routes(kwargs['routes'], printer=print)
        print('')

    return kwargs


def AutoApp(**kwargs):
    return App(**app_args(**kwargs))


def AutoASyncApp(**kwargs):
    return ASyncApp(**app_args(**kwargs))
