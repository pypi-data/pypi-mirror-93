# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['inshorts']
install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'inshorts',
    'version': '2021.1',
    'description': 'cli for inshorts',
    'long_description': None,
    'author': 'Sayan Goswami',
    'author_email': 'goswami.sayan47@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
