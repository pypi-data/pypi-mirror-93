# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minimal_cernsso']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2,<3', 'six>=1.15,<2.0']

entry_points = \
{'console_scripts': ['cernsso-get-cookies = minimal_cernsso:cli_get_cookies']}

setup_kwargs = {
    'name': 'minimal-cernsso',
    'version': '0.0.1',
    'description': 'Minimal implementation of getting a CERN SSO cookie',
    'long_description': None,
    'author': 'Thomas Klijnsma',
    'author_email': 'tklijnsm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
