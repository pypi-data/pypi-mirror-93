# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nomnomdata', 'nomnomdata.cli', 'nomnomdata.cli.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'coloredlogs>=14.0,<15.0',
 'dunamai>=1.1.0,<2.0.0',
 'packaging>=20.4,<21.0',
 'requests>=2.23.0,<3.0.0',
 'rich>=9.0.0,<10.0.0']

entry_points = \
{'console_scripts': ['nnd = nomnomdata.cli.cli:main']}

setup_kwargs = {
    'name': 'nomnomdata-cli',
    'version': '0.1.10',
    'description': 'Package containing tooling for developing nominode engines',
    'long_description': '',
    'author': 'Nom Nom Data Inc',
    'author_email': 'info@nomnomdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nomnomdata/tools/nomnomdata-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
