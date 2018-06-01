import inspect
import logging
import os
import typing
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


def process_app_routes(app, prefix: typing.Union[str, tuple] = None):
    """
    For a given dict of app data figure out if the app is nested
    and if so convert the routes to an Include with the appropriate
    URL prefix.
    """

    routes = app.get('routes')
    app_path = app.get('app_path')
    inc_name = ''
    url_prefix = '/'

    # If the app has no routes or is not nested (no or empty app_path), do nothing.
    if not routes or not app_path:
        return app

    if isinstance(prefix, tuple):
        url_prefix = prefix[0]
        if len(prefix) == 2:
            inc_name = prefix[1] + ':'
    elif prefix:
        url_prefix = prefix

    if url_prefix[-1] != '/':
        url_prefix += '/'

    inc_name += ':'.join(app_path)

    # Build an Include for the set of nested URLs with the matching prefix
    # for the directory structure
    # If a prefix param is present, pre-pend it as well
    app['routes'] = [Include(
        url_prefix + '/'.join(app_path),
        name=inc_name,
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


def prioritize(priority_app_paths, reg_apps):
    if not priority_app_paths:
        return reg_apps

    # Sort the reg_apps so the priority_apps are honored and first
    priority_apps = []
    # Don't mutate the original list of apps, we'll return
    # the prioritized list as a new list
    apps = reg_apps.copy()

    for papp in priority_app_paths:
        papp_path = tuple(papp.split('.'))

        for app in apps:
            if papp_path == app.get('app_path', tuple()):
                priority_apps.append(app)
                apps.remove(app)

    return priority_apps + apps


def app_args(project_dir: str = None,
             apps: list = None,
             priority_apps: list = None,
             print_results: bool = False,
             routes_prefix: typing.Union[str, tuple] = None,
             **kwargs) -> dict:

    sub_routes = []
    sub_comps = []
    sub_hooks = []

    # The apps list takes priority over the auto found apps,
    # but priority can be adjusted with priority_apps
    explicit_apps = [inspect_app((app,)) for app in apps or []]

    project_dir = project_dir or find_caller_dir()

    # Find all the sub apps and collect their info then prioritize them
    # along with the explicit apps
    apps = prioritize(
        priority_apps,
        explicit_apps + find_apps(os.path.realpath(project_dir))
    )

    # Collect and process all the imported app data
    for app in apps:
        app = process_app_routes(app, prefix=routes_prefix)
        sub_routes += app.get('routes', [])
        sub_comps += app.get('components', [])
        sub_hooks += app.get('event_hooks', [])

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
