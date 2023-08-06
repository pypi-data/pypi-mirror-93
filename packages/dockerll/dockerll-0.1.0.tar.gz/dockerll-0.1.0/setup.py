# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockerll']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['dockerll = dockerll.__main__:run']}

setup_kwargs = {
    'name': 'dockerll',
    'version': '0.1.0',
    'description': 'Docker layer labeler - put tags on the intermediary stages of a multistage docker build',
    'long_description': None,
    'author': 'Mardoqueu Pimentel',
    'author_email': 'mardoqueu.pimentel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
