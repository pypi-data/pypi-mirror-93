# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcdrtelegram']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.11.2,<3.0.0', 'ujson>=4.0.2,<5.0.0', 'uvloop>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'mcdrtelegram',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Yi-Jyun Pan',
    'author_email': 'pan93412@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
