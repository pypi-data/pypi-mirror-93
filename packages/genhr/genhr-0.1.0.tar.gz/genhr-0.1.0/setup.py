# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genhr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'genhr',
    'version': '0.1.0',
    'description': 'Create zipped test files to upload to HackerRank',
    'long_description': None,
    'author': 'Thomas Breydo',
    'author_email': 'tbreydo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
