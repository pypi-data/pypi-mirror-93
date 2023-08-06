# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rodder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rodder',
    'version': '0.1.0',
    'description': 'A distro-independant package manager for Linux',
    'long_description': None,
    'author': 'Drake',
    'author_email': 'mdrakea3@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
