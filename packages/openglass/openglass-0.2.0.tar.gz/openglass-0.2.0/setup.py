# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openglass']

package_data = \
{'': ['*']}

install_requires = \
['Telethon>=1.17.5,<2.0.0', 'six>=1.15.0,<2.0.0', 'tweepy>=3.9.0,<4.0.0']

entry_points = \
{'console_scripts': ['openglass = openglass:main']}

setup_kwargs = {
    'name': 'openglass',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Hiro',
    'author_email': 'hiro@torproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
