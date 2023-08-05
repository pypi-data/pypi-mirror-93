# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jwa']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jwa = jwa.__init__:card']}

setup_kwargs = {
    'name': 'jwa',
    'version': '2021.1',
    'description': 'pipx run jwa',
    'long_description': None,
    'author': 'Julian Wachholz',
    'author_email': 'julian@wachholz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
