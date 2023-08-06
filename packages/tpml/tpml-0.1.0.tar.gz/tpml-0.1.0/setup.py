# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tpml']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.4,<4.0.0',
 'multipledispatch>=0.6.0,<0.7.0',
 'numpy>=1.20.0,<2.0.0',
 'typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'tpml',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tom Pinder',
    'author_email': 'tompinder@live.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
