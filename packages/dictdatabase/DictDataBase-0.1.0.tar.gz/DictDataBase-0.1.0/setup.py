# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dictdatabase']

package_data = \
{'': ['*']}

install_requires = \
['path-dict>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'dictdatabase',
    'version': '0.1.0',
    'description': 'Easy-to-use database using dicts',
    'long_description': None,
    'author': 'Marcel Kröker',
    'author_email': 'kroeker.marcel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
