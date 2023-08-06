# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['self_make']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'self-make',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'fandong',
    'author_email': 'fandong@coding.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
