# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['klickbrick_codeangler']

package_data = \
{'': ['*']}

install_requires = \
['behave>=1.2.6,<2.0.0']

entry_points = \
{'console_scripts': ['klickbrick = klickbrick_codeangler.main:main']}

setup_kwargs = {
    'name': 'klickbrick-codeangler',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'caseyburnett',
    'author_email': 'casey.burnett@davita.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codeangler/liveproject-cli-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
