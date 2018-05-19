
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


* [Features](#features)
* [Quickstart](#quickstart)
* [Docs](#docs)


## Features


## Quickstart

```python
from apistar-autoapp import AutoApp

async def welcome() -> dict:
    return {'msg': 'hello'}


routes = [
    Route('/', 'GET', handler=welcome, name='welcome'),
]

app = AutoApp(routes=routes)

def main():
    app.serve('127.0.0.1', 8000, debug=True)


if __name__ == '__main__':
    main()
```


## Docs


### Print helpers
