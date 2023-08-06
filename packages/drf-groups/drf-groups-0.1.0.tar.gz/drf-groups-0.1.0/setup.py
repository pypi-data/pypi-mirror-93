# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_groups']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.11.0']

setup_kwargs = {
    'name': 'drf-groups',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@sourcelair.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
