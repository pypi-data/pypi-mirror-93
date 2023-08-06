# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['line_buto']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'line-buto',
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
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
