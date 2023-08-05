#!/usr/bin/env python

import os
import io
import re
from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(root_path):
    version = ""
    with open(os.path.join(root_path, 'VERSION')) as version_file:
        version = version_file.read().strip()

    if len(version) > 1:
        return version
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

PACKAGE = 'hexonet.ispapicli'
VERSION = find_version(os.path.dirname(__file__))

setup(
    name=PACKAGE,
    version=VERSION,
    description=PACKAGE + ' is a command line client library for the insanely fast HEXONET Backend API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Rashad Jamara',
    author_email='rjamara@hexonet.net',
    maintainer='Rashad Jamara',
    maintainer_email='rjamara@hexonet.net',
    url='https://github.com/hexonet/ispapicli/',
    install_requires=[
        'altgraph>=0,<1',
        'autopep8>=1,<2',
        'beautifulsoup4>=4,<5',
        'certifi>=2020,<2021',
        'chardet>=3,<4',
        'hexonet.apiconnector>=3,<4',
        'idna>=2,<3',
        'numpy>=1,<2',
        'pep8>=1,<2',
        'Pillow>=7,<8',
        'pycodestyle>=2,<3',
        'PyQt5>=5,<6',
        'PyQt5-sip>=12,<13',
        'requests>=2,<3',
        'soupsieve>=2,<3',
        'tabulate>=0,<1'
        'urllib3>=1,<2'
        'twine>=3,<4'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    license="MIT",
    scripts=[],
    zip_safe=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
    namespace_packages=['hexonet'],
    packages=find_packages(),
    python_requires='>=3.6',
    package_data={
        '': ['*.json', '*.png']
    }
)
