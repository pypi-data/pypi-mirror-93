# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_api']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['deepl = deepl_api.cli:run']}

setup_kwargs = {
    'name': 'deepl-api',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Martin Gruner',
    'author_email': 'mg.pub@gmx.net',
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
