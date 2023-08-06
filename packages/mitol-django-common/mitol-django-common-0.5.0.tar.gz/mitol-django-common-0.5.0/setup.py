# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitol',
 'mitol.common',
 'mitol.common.factories',
 'mitol.common.management',
 'mitol.common.management.commands',
 'mitol.common.settings',
 'mitol.common.templatetags',
 'mitol.common.utils']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2.12,<3.2',
 'django-webpack-loader>=0.7.0,<0.8.0',
 'psycopg2-binary>=2.8.3,<3.0.0',
 'requests>=2.20.0,<3.0.0']

extras_require = \
{'dev': ['ipython>=7.13.0,<8.0.0'],
 'test': ['pytest>=6.0.2,<7.0.0',
          'pytest-cov',
          'pytest-mock==1.10.1',
          'pytest-django==3.10.0',
          'freezegun>=1.0.0,<2.0.0',
          'factory_boy>=3.0.0,<4.0.0',
          'responses>=0.12.0,<0.13.0',
          'coverage==5.3.1',
          'isort>=4.3.21,<5.0.0',
          'black>=19.10b0,<20.0',
          'pylint>=2.0,<3.0',
          'pylint-django>=2.0.2,<3.0.0',
          'mypy>=0.782,<0.783',
          'django-stubs==1.6.0']}

setup_kwargs = {
    'name': 'mitol-django-common',
    'version': '0.5.0',
    'description': 'MIT Open Learning django app extensions for common utilities',
    'long_description': None,
    'author': 'MIT Office of Open Learning',
    'author_email': 'mitx-devops@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
