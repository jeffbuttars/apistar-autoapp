import inspect
import os


def cur_dir():
    frame = inspect.stack()[0]
    return os.path.dirname(frame.filename)
