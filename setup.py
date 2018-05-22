import os
import re

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('apistar_autoapp')


setup(
    name='apistar-autoapp',
    version=version,
    description='Automatically import APIStar sub apps',
    url='git@github.com:jeffbuttars/apistar-autoapp',
    author='Jeff Buttars',
    license='Apache',
    packages=['apistar_autoapp'],
    install_requires=[
        'apistar',
        'whitenoise',
        'aiofiles',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
