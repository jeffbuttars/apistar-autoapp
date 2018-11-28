#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
import os
import re

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_long_description(long_description_file):
    """
    Read long description from file.
    """
    with open(long_description_file, encoding='utf-8') as f:
        long_description = f.read()

    return long_description


version = get_version('apistar_autoapp')


setup(
    name='apistar-autoapp',
    version=version,
    url='https://github.com/jeffbuttars/apistar-autoapp',
    author='Jeff Buttars',
    author_email='jeff@jeffbuttars.com',
    license='Apache License 2.0',
    description='Automatically import APIStar sub apps',
    long_description=get_long_description('README.md'),
    long_description_content_type='text/markdown',
    packages=['apistar_autoapp'],
    install_requires=[
        'apistar<=0.5.42',
        'whitenoise',
        'aiofiles',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
