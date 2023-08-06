# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pysimpletime']
setup_kwargs = {
    'name': 'pysimpletime',
    'version': '2.0.0',
    'description': 'Easy realtime debugging with time results',
    'long_description': None,
    'author': 'James Frienkins',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
