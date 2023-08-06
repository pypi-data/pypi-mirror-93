# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pheidi']

package_data = \
{'': ['*']}

install_requires = \
['msgpack-numpy>=0.4.7,<0.5.0', 'msgpack>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'pheidi',
    'version': '0.0.15',
    'description': 'Fast In Ram Memory',
    'long_description': None,
    'author': 'Austin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
