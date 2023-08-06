# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colette']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11,<3.0', 'mip>=1.13,<2.0']

entry_points = \
{'console_scripts': ['colette = colette.__main__:main']}

setup_kwargs = {
    'name': 'colette',
    'version': '0.1.0',
    'description': 'Manage rounds of coffee roulette',
    'long_description': None,
    'author': 'David Horsley',
    'author_email': 'david.e.horsley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
