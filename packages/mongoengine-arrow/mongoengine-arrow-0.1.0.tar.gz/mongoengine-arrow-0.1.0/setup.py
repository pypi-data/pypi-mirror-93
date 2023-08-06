# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongoengine_arrow']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17.0,<0.18.0', 'mongoengine>=0.22.1,<0.23.0']

setup_kwargs = {
    'name': 'mongoengine-arrow',
    'version': '0.1.0',
    'description': 'Arrow datetime support for MongoEngine',
    'long_description': None,
    'author': 'Niko Järvinen',
    'author_email': 'nbjarvinen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
