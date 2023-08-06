# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['inmanta_dev_dependencies']

package_data = \
{'': ['*']}

install_requires = \
['black==20.8b1',
 'flake8-black==0.2.1',
 'flake8-copyright==0.2.2',
 'flake8-isort==4.0.0',
 'flake8==3.8.4',
 'isort==5.7.0',
 'lxml==4.6.2',
 'mypy==0.800',
 'pep8-naming==0.11.1',
 'pytest==6.2.2']

extras_require = \
{'async': ['pytest-asyncio==0.14.0', 'pytest-timeout==1.4.2'],
 'extension': ['pytest-inmanta-extensions==2020.5.1',
               'asyncpg==0.21.0',
               'click==7.1.2',
               'pyformance==0.4',
               'pytest-env==0.6.2',
               'pytest-postgresql==2.5.3',
               'psycopg2==2.8.6',
               'tornado==6.1',
               'tornado==6.1',
               'tox==3.21.3',
               'tox-venv==0.4.0'],
 'module': ['pytest-inmanta==1.4.0'],
 'pytest': ['pytest-env==0.6.2',
            'pytest-cover==3.0.0',
            'pytest-randomly==3.5.0',
            'pytest-xdist==2.2.0',
            'pytest-sugar==0.9.4',
            'pytest-sugar==0.9.4',
            'pytest-instafail==0.4.2',
            'pytest-instafail==0.4.2']}

setup_kwargs = {
    'name': 'inmanta-dev-dependencies',
    'version': '1.13.0',
    'description': 'Package collecting all common dev dependencies of inmanta modules and extensions to synchronize dependency versions.',
    'long_description': None,
    'author': 'Inmanta',
    'author_email': 'code@inmanta.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
