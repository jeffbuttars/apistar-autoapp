
<p align='center'>
    <H1 align='center'> APIStar AutoApp </H1>
</p>

<p align='center'>
    <em>Easily manage and compose larger APIStar projects</em>
</p>

<p align='center'>
    <img alt='CircleCI Test Status' src='https://circleci.com/gh/jeffbuttars/apistar-autoapp.svg?style=shield&circle-token=dab68c7748dee073e7176628ab35652fd5c7cae6' />
</p>


---


Automatically orchestrates [APIStar](https://docs.apistar.com/) projects with sub modules using an
`app` based pattern.


* [Features](#features)
* [Quickstart](#quickstart)
* [Install](#install)
* [Docs](#docs)
    * [AutoApp](#autoapp)
    * [AutoASyncApp](#autoasyncapp)
    * [app_args](#app_args)
    * [Print Helper](#print-helper)
        * [include](#include)
        * [route](#route)
        * [routes](#routes)
        * [components](#components)


## Features




* Automatically [Includes routes](https://docs.apistar.com/api-guide/routing/#routing-in-larger-projects) from `app`s creating the appropriate URL based on the
    filesystem path from the projects root `app.py` file.
* Automatically collect [event_hooks](https://docs.apistar.com/api-guide/event-hooks/) and [component](https://docs.apistar.com/api-guide/dependency-injection/) lists from apps and consolidate them
  together to build the [App](https://docs.apistar.com/api-guide/applications/)/[ASyncApp](https://docs.apistar.com/api-guide/applications/) with.
* Allow an ordered priority list of apps by their path string to control the order of items
  in the [event_hooks](https://docs.apistar.com/api-guide/event-hooks/) and [component](https://docs.apistar.com/api-guide/dependency-injection/) lists as well as control import order.



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

## Install

    pip install apistar-autoapp

or for [Pipenv](https://docs.pipenv.org/) users

    pipenv install apistar-autoapp



## Docs

### AutoApp

    AutoApp(project_dir: str = None,
            priority_apps: list = None,
            print_results: bool = False,
            **kwargs) -> App


### AutoASyncApp

    AutoASyncApp(project_dir: str = None,
                 priority_apps: list = None,
                 print_results: bool = False,
                 **kwargs) -> ASyncApp


### app_args

    app_args(project_dir: str = None,
             priority_apps: list = None,
             print_results: bool = False,
             **kwargs) -> dict:

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
