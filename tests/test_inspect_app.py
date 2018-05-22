import os
import sys
import importlib
#  import inspect
import pytest
from apistar_autoapp.autoapp import inspect_app


def test_inspect_app_top():
    with pytest.raises(TypeError):
        inspect_app()

    with pytest.raises(ModuleNotFoundError):
        inspect_app(tuple())

    importlib.import_module('tests.app')

    res = inspect_app(('tests',))
    assert res
    print('test_inspect_app_top', res)
