# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['attrsfile']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'cattrs>=1.1.2,<2.0.0',
 'pre-commit>=2.10.0,<3.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'attrsfile',
    'version': '0.1.1',
    'description': 'A file mapper for attrs classes.',
    'long_description': None,
    'author': 'Deniz Bozyigit',
    'author_email': 'deniz195@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
