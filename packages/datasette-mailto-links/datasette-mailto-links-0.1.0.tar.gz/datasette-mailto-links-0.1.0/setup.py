# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasette_mailto_links']

package_data = \
{'': ['*']}

install_requires = \
['datasette>0']

entry_points = \
{'datasette': ['mailto_links = datasette_mailto_links']}

setup_kwargs = {
    'name': 'datasette-mailto-links',
    'version': '0.1.0',
    'description': 'Datasette plugin to render email addresses as mailto: links',
    'long_description': '# datasette-mailto-links\n\n![Run tests](https://github.com/chris48s/datasette-mailto-links/workflows/Run%20tests/badge.svg?branch=main)\n[![codecov](https://codecov.io/gh/chris48s/datasette-mailto-links/branch/main/graph/badge.svg?token=JEUG9Y0ZT3)](https://codecov.io/gh/chris48s/datasette-mailto-links)\n[![PyPI Version](https://img.shields.io/pypi/v/datasette-mailto-links.svg)](https://pypi.org/project/datasette-mailto-links/)\n![License](https://img.shields.io/pypi/l/datasette-mailto-links.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdatasette-mailto-links%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nDatasette plugin to render email addresses as `mailto:` links\n\n## Installation\n\n```\npip install datasette-mailto-links\n```\n\n## Configuration\n\nBy default, when installed datasette-mailto-links will search for values in any column that look like an email address and replace them with a `mailto:` link. To restrict this behaviour to only certain columns, the plugin behaviour can be configured in `metadata.json`. e.g:\n\n```json\n{\n  "databases": {\n    "my_db": {\n      "tables": {\n        "email": {\n          "plugins": {\n            "datasette-mailto-links": {\n              "columns": ["sender", "recipient"]\n            }\n          }\n        }\n      }\n    }\n  }\n}\n```\n\nThe plugin can be disabled entirely for certain tables using `"columns": []`\n\nFor more detail on Datasette plugin configuration see https://docs.datasette.io/en/latest/plugins.html#plugin-configuration\n',
    'author': 'chris48s',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chris48s/datasette-mailto-links',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
