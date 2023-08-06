# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ythesis']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ythesis',
    'version': '0.1.1',
    'description': 'provides thesis entities',
    'long_description': 'ythesis\n================================================================================\n',
    'author': 'yassu',
    'author_email': 'yasu0320.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/yassu/ythesis',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
