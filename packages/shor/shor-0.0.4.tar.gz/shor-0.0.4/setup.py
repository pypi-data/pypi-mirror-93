# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shor',
 'shor.algorithms',
 'shor.providers',
 'shor.providers.qiskit',
 'shor.transpilers',
 'shor.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0', 'numpy>=1.19.4,<2.0.0', 'qiskit>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'shor',
    'version': '0.0.4',
    'description': 'Quantum Computing for Humans',
    'long_description': None,
    'author': 'Collin Overbay - shor.dev',
    'author_email': 'shordotdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
