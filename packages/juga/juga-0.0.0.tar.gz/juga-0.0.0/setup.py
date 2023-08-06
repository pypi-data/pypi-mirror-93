# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['juga']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['juga = juga.__init__:run_cli']}

setup_kwargs = {
    'name': 'juga',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Chanwoong Kim',
    'author_email': 'me@chanwoong.kim',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
