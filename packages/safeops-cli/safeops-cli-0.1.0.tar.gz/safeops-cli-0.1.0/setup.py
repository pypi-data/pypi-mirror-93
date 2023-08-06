# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cli']
install_requires = \
['click>=7.1.2,<8.0.0', 'funcy>=1.15,<2.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['safeops = cli:process']}

setup_kwargs = {
    'name': 'safeops-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andres moreno',
    'author_email': 'amoreno@opsline.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
