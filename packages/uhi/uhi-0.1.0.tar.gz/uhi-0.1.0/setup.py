# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['uhi', 'uhi.typing']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7,<4.0'],
 'docs': ['sphinx==3', 'sphinx-rtd-theme>=0.5.1,<0.6.0'],
 'test': ['pytest>=5.2,<6.0']}

setup_kwargs = {
    'name': 'uhi',
    'version': '0.1.0',
    'description': 'Unified Histogram Indexing',
    'long_description': None,
    'author': 'Henry Schreiner',
    'author_email': 'henryschreineriii@gmail.com',
    'maintainer': 'The Scikit-HEP admins',
    'maintainer_email': 'scikit-hep-admins@googlegroups.com',
    'url': 'https://github.com/Scikit-HEP/uhi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
