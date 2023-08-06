# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yamlett']

package_data = \
{'': ['*']}

install_requires = \
['fastcore>=1.3.9,<2.0.0', 'pymongo>=3.11.1,<4.0.0']

setup_kwargs = {
    'name': 'yamlett',
    'version': '0.0.1',
    'description': 'Yet Another ML Experiment Tracking Tool',
    'long_description': None,
    'author': 'Virgile Landeiro',
    'author_email': 'virgile.landeiro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
