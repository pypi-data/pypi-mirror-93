# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weasel_data_sources']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'weasel-data-sources',
    'version': '0.1.1',
    'description': '`weasel-data-sources` is a collection of data sources to retrieve information about software releases and vulnerabilities.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
