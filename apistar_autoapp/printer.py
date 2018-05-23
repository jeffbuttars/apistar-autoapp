import inspect

_tab = '  '


def _sig(func) -> str:
    argspec = inspect.getfullargspec(func)

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

    return (args_str, return_str)


class Printer(object):
    def __init__(self, printer=None):
        self._pr = printer or print

    def include(self, include, level: int = 0):
        self._pr('{}Include: {} {}'.format(_tab * level, include.url, include.name))

        for route in include.routes:
            self.route(route, parent_url=include.url, level=level + 1)

    def route(self, route, parent_url: str = None, level: int = 0):
        url = parent_url + route.url if parent_url else route.url

        args_str, return_str = _sig(route.handler)

        route_handler = route.handler.__module__ + '.' + route.handler.__qualname__
        route_handler = '{}.{}({}){}'.format(
            route.handler.__module__, route.handler.__qualname__, args_str, return_str
        )

        self._pr('{}Route: {:>3} {}, {}'.format(_tab * level, route.method, url, route.name))
        self._pr('{} {}'.format(_tab * (level + 3), route_handler))

    def routes(self, routes):
        self._pr('\nRoutes:')

        for route in routes:
            if hasattr(route, 'routes'):
                self.include(route, level=1)
            else:
                self.route(route, level=1)

    def components(self, components):
        self._pr('\nComponents:')
        for comp in components:
            args_str, return_str = _sig(comp.resolve)
            self._pr('\t{}'.format(comp.__class__.__name__))
            self._pr('\t\tresolve({}){}'.format(args_str, return_str))
