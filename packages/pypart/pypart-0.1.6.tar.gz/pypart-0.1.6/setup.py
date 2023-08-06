# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pypart']
install_requires = \
['pandas>=1.1.0,<2.0.0', 'pipelinehelper>=0.7.8,<0.8.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'pypart',
    'version': '0.1.6',
    'description': 'Couples pipeline transformers with their parameters for easier reuse of transformers',
    'long_description': None,
    'author': 'Benjamin Murauer',
    'author_email': 'b.murauer@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
