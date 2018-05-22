import os
import inspect


def cur_dir():
    frame = inspect.stack()[0]
    module = inspect.getmodule(frame[0])
    return os.path.dirname(os.path.realpath(module.__file__))
