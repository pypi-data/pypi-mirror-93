# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['host_api']

package_data = \
{'': ['*'], 'host_api': ['.deta/*']}

install_requires = \
['bcrypt>=3.2.0,<4.0.0',
 'deta>=0.7,<0.8',
 'fastapi>=0.63.0,<0.64.0',
 'passlib>=1.7.4,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-jose>=3.2.0,<4.0.0',
 'typer>=0.3.2,<0.4.0',
 'uvicorn>=0.13.3,<0.14.0']

entry_points = \
{'console_scripts': ['webhost = host_api.main:webapp']}

setup_kwargs = {
    'name': 'host.api',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
