# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rodder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rodder',
    'version': '0.1.2',
    'description': 'A distro-independant package manager for Linux',
    'long_description': '# rodder\nA distro-independent (or distro-agonistic if you wanna be fancy), non-system package manager with custom repos, similar to Homebrew\n\n# FAQ\n\n## Why "rodder"?\nBecause a fishing rod grabs fish, similar to how a package manager grabs packages.\n',
    'author': 'Drake',
    'author_email': 'mdrakea3@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ruthenic/rodder',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
