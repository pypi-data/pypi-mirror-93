# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonapy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonapy',
    'version': '0.1.1',
    'description': 'Library for dumping models into JSON:API',
    'long_description': 'Dumping JSON:API in Python\n==========================\n\n`jsonapy` is a Python library for dumping models into JSON:API-compliant JSON.\n\n',
    'author': 'Guillaume Fayard',
    'author_email': 'guillaume.fayard@pycolore.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arkelis/jsonapy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
