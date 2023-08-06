# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sondehub']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['sondehub = sondehub:__main__.main']}

setup_kwargs = {
    'name': 'sondehub',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Michaela',
    'author_email': 'git@michaela.lgbt',
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
