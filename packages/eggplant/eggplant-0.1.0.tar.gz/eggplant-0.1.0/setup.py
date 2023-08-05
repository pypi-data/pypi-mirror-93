# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eggplant']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'psycopg2>=2.8.6,<3.0.0',
 'royalnet>=6.0.2,<7.0.0',
 'sqlalchemy>=1.3.22,<2.0.0',
 'uvicorn>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'eggplant',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
