import inspect
import logging
import os
from importlib import import_module

from apistar import App, ASyncApp, Include

from .printer import Printer

logger = logging.getLogger('autoapp')


def find_caller_dir():
    """
    This does a little work beyond relying on the caller always
    being at a certain point in the call stack.
    The algorithm is as such:
        * prefer the first module who's filename is app.py
        * otherwise is no app.py is found, use the first module that is
          not this module
    """
    closest_frame = None
    this_file = os.path.basename(__file__)

    for frame in inspect.stack():
        if os.path.basename(frame.filename) == 'app.py':
            return os.path.dirname(frame.filename)

        if not closest_frame and os.path.basename(frame.filename) != this_file:
            closest_frame = frame

    # Didn't find an `app.py`, return the first thing not this.
    if closest_frame:
        return os.path.dirname(closest_frame.filename)

    raise ImportError('Unable to find calling module')


def list_apps(app_dir: str) -> list:
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


def find_apps(cur_dir: str, parent_app: tuple = None):
    res = []

    sub_apps = list_apps(cur_dir)
    parent_app = parent_app if parent_app else tuple()

    for app_name in sub_apps:
        app_path = parent_app + (app_name,)
        cur_app = inspect_app(app_path)

        # Decend into each found app
        sub_res = find_apps(os.path.join(cur_dir, app_name), app_path)
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

    project_dir = project_dir or find_caller_dir()

    # Find all the sub apps and collect their info then prioritize them
    sub_apps = prioritize(
        priority_apps,
        find_apps(os.path.realpath(project_dir))
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
        pr = Printer()
        pr.components(kwargs['components'])
        pr.routes(kwargs['routes'])
        print('')

    return kwargs


def AutoApp(**kwargs) -> App:
    return App(**app_args(**kwargs))


def AutoASyncApp(**kwargs) -> ASyncApp:
    return ASyncApp(**app_args(**kwargs))
