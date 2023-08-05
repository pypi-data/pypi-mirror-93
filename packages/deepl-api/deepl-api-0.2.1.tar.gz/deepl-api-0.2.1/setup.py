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
    'version': '0.2.1',
    'description': 'Bindings and a commandline tools for the DeepL REST API (https://www.deepl.com/docs-api/)',
    'long_description': '# deepl-api-py\n\nThis repository contains a [Python](https://www.python.org/) implementation of the [DeepL REST API](https://www.deepl.com/docs-api/).\n\n## Contents\n\n- A [Python package](https://mgruner.github.io/deepl-api-py-docs/deepl_api/index.html) for easy integration into Python applications.\n- The `deepl` [unix-style commandline application](https://mgruner.github.io/deepl-api-py-docs/deepl_api/cli.html) for integration into existing toolchains without any programming effort.\n- Unit and integration tests.\n\nPlease refer to the linked documentation for instructions on how to get started with the API and/or the CLI tool.\n\n## Features\n\n- Query your account usage & limits information.\n- Fetch the list of available source and target languages provided by DeepL.\n- Translate text.\n\n## Not Implemented\n\n- Support for the [(beta) document translation endpoint](https://www.deepl.com/docs-api/translating-documents/).\n- Support for the [XML handling flags](https://www.deepl.com/docs-api/translating-text/) in the translation endpoint.',
    'author': 'Martin Gruner',
    'author_email': 'mg.pub@gmx.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mgruner/deepl-api-py/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
