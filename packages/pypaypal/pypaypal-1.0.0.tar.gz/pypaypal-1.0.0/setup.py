"""
Copyright (C) 2020 Ivan Cuello

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author:
    Ivan Cuello <ivcuello@gmail.com>
"""

import os
import sys

import pathlib
from setuptools import setup, find_packages

# Current folder and README.md
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

CURRENT_PYTHON_VERSION = sys.version_info[:2]
REQUIRED_PYTHON_VERSION = (3,6)

# Validating python version before the setup run
if REQUIRED_PYTHON_VERSION > CURRENT_PYTHON_VERSION:
    sys.stderr.write("""
    Unsupported python version found.

    Current Python: {}.
    Required Python: {}.
    
    """.format(CURRENT_PYTHON_VERSION, REQUIRED_PYTHON_VERSION))
    sys.exit(64)

setup(
    name='pypaypal',
    version='1.0.0',
    python_requires='>=3.6',
    author='ivcuello',
    author_email='ivcuello@gmail.com',
    url='https://github.com/ivcuello/pypaypal',
    description='Paypal API integration supporting some v1 & most of the current v2 rest APIs calls',
    long_description=README,
    long_description_content_type="text/markdown",    
    packages = find_packages(exclude=['docs', 'tests']),
    install_requires = [ 
        'python-dateutil',
        'requests'
    ],
    license="Apache License 2.0",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ]
)
