# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aopi',
 'aopi.application',
 'aopi.models',
 'aopi.routes',
 'aopi.routes.api',
 'aopi.routes.api.admin',
 'aopi.routes.api.auth',
 'aopi.routes.api.packages',
 'aopi.runners',
 'aopi.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'aiosqlite>=0.16.0,<0.17.0',
 'aopi-index-builder>=0.1.40,<0.2.0',
 'argon2-cffi>=20.1.0,<21.0.0',
 'argparse-utils>=1.3.0,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'httptools>=0.1.1,<0.2.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-jose>=3.2.0,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'tabulate>=0.8.7,<0.9.0',
 'ujson>=4.0.1,<5.0.0',
 'uvicorn>=0.13.3,<0.14.0']

extras_require = \
{'mysql': ['aiomysql>=0.0.21,<0.0.22', 'mysqlclient>=2.0.2,<3.0.0'],
 'postgre': ['asyncpg>=0.21.0,<0.22.0', 'psycopg2>=2.8.6,<3.0.0'],
 'python': ['aopi-python>=0.1.21,<0.2.0'],
 'unix': ['uvloop>=0.14.0,<0.15.0', 'gunicorn>=20.0.4,<21.0.0']}

entry_points = \
{'console_scripts': ['aopi = aopi.main:main']}

setup_kwargs = {
    'name': 'aopi',
    'version': '0.1.16',
    'description': 'Another one package index for humans',
    'long_description': 'Another one package index\n=========================\n\nThis project is under development.',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aopi-project/aopi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
