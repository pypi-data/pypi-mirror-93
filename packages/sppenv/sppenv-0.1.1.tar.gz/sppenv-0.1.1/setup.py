# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sppenv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sppenv',
    'version': '0.1.1',
    'description': 'Simplified Python `.env` file parser.',
    'long_description': '# penv\n\nSimplified Python `.env` file parser.',
    'author': 'TheBoringDude',
    'author_email': 'iamcoderx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
