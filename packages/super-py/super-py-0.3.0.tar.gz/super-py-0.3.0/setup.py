# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['super_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'super-py',
    'version': '0.3.0',
    'description': 'Features that Python should have in the standard library',
    'long_description': '# SuperPy\n\nDescription follows (Or look into the files, its not that complicated)',
    'author': 'Marcel Kröker',
    'author_email': 'kroeker.marcel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
