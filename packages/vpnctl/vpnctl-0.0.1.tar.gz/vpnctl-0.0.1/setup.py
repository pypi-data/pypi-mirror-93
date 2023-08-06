# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vpnctl']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['vpnctl = vpnctl:main']}

setup_kwargs = {
    'name': 'vpnctl',
    'version': '0.0.1',
    'description': 'A simple command line interface for managing and controlling VPN connections.',
    'long_description': '# vpnctl\n\nA simple command line interface for managing and controlling VPN connections.\n\n## Goals\n\nThis project strives to simplify interaction with VPN tools through the command\nline. It will first support OpenVPN connections but may be expanded later. \nIts primary focus is on Unix and Mac users.\n\n* * *\n\n&copy; 2021 Robert Mörseburg -- Licensed under the [MIT License](./LICENSE).\n',
    'author': 'Robert Mörseburg',
    'author_email': 'fl4m@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fl4m/vpnctl',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
