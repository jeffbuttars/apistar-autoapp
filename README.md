
<p align='center'>
    <H1 align='center'> API Star AutoApp </H1>
</p>

<p align='center'>
    <em>Easily manage and compose API Star projects</em>
</p>

<p align='center'>
    <img alt='CircleCI Test Status' src='https://circleci.com/gh/jeffbuttars/apistar-autoapp.svg?style=shield&circle-token=dab68c7748dee073e7176628ab35652fd5c7cae6' />
    <a href="https://badge.fury.io/py/apistar-autoapp">
    <img src="https://badge.fury.io/py/apistar-autoapp.svg" alt="PyPI version" height="18">
    </a>
</p>


---


Automatically orchestrates [API Star](https://docs.apistar.com/) projects with sub modules using an
`app` based pattern.


* [Features](#features)
* [Quickstart](#quickstart)
* [Install](#install)
* [Anatomy](#anatomy)
    * [Example project structure](#example-project-structure)
* [Docs](#docs)
    * [AutoApp](#autoapp)
    * [AutoASyncApp](#autoasyncapp)
    * [app_args](#app_args)
    * [Print Helper](#print-helper)
        * [include](#include)
        * [route](#route)
        * [routes](#routes)
        * [components](#components)
* [TODO](#todo)

---

## Features


* Automatically build URLs based on your project's structure.
    * Autoapp [Includes routes](https://docs.apistar.com/api-guide/routing/#routing-in-larger-projects)
        from apps in your project creating the appropriate URL based on the
        filesystem path from the projects root `app.py` file.
* Automatically collect [event_hooks](https://docs.apistar.com/api-guide/event-hooks/) and [component](https://docs.apistar.com/api-guide/dependency-injection/) lists from apps and consolidate them
  together to build the [App](https://docs.apistar.com/api-guide/applications/)/[ASyncApp](https://docs.apistar.com/api-guide/applications/) with.
* Allow an ordered priority list of apps by their path string to control the order of items
  in the [event_hooks](https://docs.apistar.com/api-guide/event-hooks/) and [component](https://docs.apistar.com/api-guide/dependency-injection/) lists as well as control import order.


---

## Quickstart

Just use `AutoApp` or `AutoASyncApp` in place of [App](https://docs.apistar.com/api-guide/applications/) and [ASyncApp](https://docs.apistar.com/api-guide/applications/) respectively

```python
from apistar-autoapp import AutoApp

async def welcome() -> dict:
    return {'msg': 'hello'}


routes = [
    Route('/', 'GET', handler=welcome, name='welcome'),
]

app = AutoApp(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 8000, debug=True)
```

---

## Install

    pip install apistar-autoapp

or for [Pipenv](https://docs.pipenv.org/) users

    pipenv install apistar-autoapp


---

## Anatomy

For a package to be considered an 'app' it must contain a file named `app.py` in it's top directory. The
`app.py` file can be empty. It's in the `app.py` file where you expose what your app
provides to the [API Star](https://docs.apistar.com/) configuration. Autoapp will look
for three attributes on the `app.py` module and if they're found add them to the [API Star](https://docs.apistar.com/)
configuration at startup.  

The attributes must be lists and named:

    routes
    components
    event_hooks

For example, a simple app that only exposes it's routes could be:

`app.py`:

    from .handlers import routes

Or an app that exposes it's routes, event_hooks and components:


`app.py`:

    from .handlers import routes
    from .components import components
    from .event_hooks import event_hooks


And of course if you have a simple app you can have all of your code in the `app.py` and
then have module variables defined by your application code.

A simple app:

```python
from apistar import App, Route


def homepage() -> str:
    return '<html><body><h1>Homepage</h1></body></html>'


routes = [
    Route('/', method='GET', handler=homepage),
]
```

### Example project structure

```

project/
  app.py
  v1/
    app.py
    ...
    endpointOne/
      app.py
      ...
    endpointTwo/
      app.py
      ...
```

If the `v1/app.py` file is empty and each of the `endpoint*` apps exposes a single root URL, `/`, route the
route URLs created for the project, via [Includes](https://docs.apistar.com/api-guide/routing/#routing-in-larger-projects)
would be:

    /v1/endpointOne
    /v1/endpointTwo

And if `endpointOne` had another route for the URL `/users`, you'd then have:

    /v1/endpointOne
    /v1/endpointOne/users
    /v1/endpointTwo

---

## Docs

### AutoApp

    AutoApp(project_dir: str = None,
            priority_apps: list = None,
            print_results: bool = False,
            **kwargs) -> App

Parameters:

    (Optional)
    project_dir: The directory from which apistar-autoapp will look for a project root.
        This is autodetected if not used and you normally won't use this parameter.

    (Optional)
    priority_apps: A list of apps, by their import path, that will be imported before all
      other apps found by apistar-autoapp and imported in the order they are given.

    (Optional)
    print_results: Print the results of the configuration created by apistar-autoapp to
      the console.

    kwargs: These are the arguments you'd normally pass to App or ASyncApp. If you pass
      any of the arguments: routes, components or event_hooks, they will be given precedence
      and listed before any of the corresponding values created by autoapp.

### AutoASyncApp

The same as [AutoApp](#autoapp) but creates a project using [ASyncApp](https://docs.apistar.com/api-guide/applications/)

    AutoASyncApp(project_dir: str = None,
                 priority_apps: list = None,
                 print_results: bool = False,
                 **kwargs) -> ASyncApp


### app_args

    app_args(project_dir: str = None,
             priority_apps: list = None,
             print_results: bool = False,
             **kwargs) -> dict:

`app_args` is the same as AutoApp and AutoASyncApp except it returns a dictionary of arguments
that are intended for use by [App](https://docs.apistar.com/api-guide/applications/) or [ASyncApp](https://docs.apistar.com/api-guide/applications/).

In fact [AutoApp](#autoapp) is just:

```python
def AutoApp(**kwargs) -> App:
    return App(**app_args(**kwargs))
```

So if you want to do something with the data from autoapp before creating your App it's easy:

```python
kwargs = app_args(...)
# Do something with kwargs
# ...
app = App(**kwargs)
```


### Print helper

There are some printing helpers for internal use by apistar-autoapp but are exposed for use by other
modules. There is a `Printer` class the uses `print` by default but can use any function that
accepts a string in it's place.

```python
from apistar_autoapp.printer import Printer

pr = Printer()

# Or if you want to your own print function, like a logger:
pr = Printer(printer=logger.info)

...

# to print out a list of routes:
pr.routes(routes)
```


#### include
Prints an [Include](https://docs.apistar.com/api-guide/routing/#routing-in-larger-projects) instance to the console as well as all of it's [Routes](https://docs.apistar.com/api-guide/routing/) in the form:

    Include: <url> <name>
        <Routes>
ex:

Include: /v2/welcome v2:welcome
    Route: GET /, welcome
           app.welcome() -> dict:

#### route
Prints a [Route](https://docs.apistar.com/api-guide/routing/) instance to the console in the form:

    Route: <method> <url>, <name>
           <handler>
ex:

    Route: GET /, welcome
           app.welcome() -> dict:

#### routes

Prints a list of [Routes](https://docs.apistar.com/api-guide/routing/) and [Includes](https://docs.apistar.com/api-guide/routing/#routing-in-larger-projects) using `print_route` and `print_include` in the form:

    Routes:
        [
            <print_route> or <print_include>,
            ...
        ]

ex:

    Routes:
        Route: GET /, welcome
               app.welcome() -> dict:
        Include: /v2/home v2:home
          Route: GET /v2/home/, list
                 v2.home.handlers.list_homes() -> list:
        ...


#### components
Prints a list of [components](https://docs.apistar.com/api-guide/dependency-injection/) in the form:


    Components:
            <ComponentClass>
                    resolve(<signature>) -> <returns>:
ex:

    Components:
            WebSocketComponent
                    resolve(self, scope: ASGIScope, send: ASGISend, receive: ASGIReceive, app: App) -> WebSocket:

---

## TODO

* Allow any package with an `app.py` file that is importable to be used with Autoapp
* Add the ability to have a list of excluded apps that will not be imported by Autoapp
* Add printer for `event_hooks`
