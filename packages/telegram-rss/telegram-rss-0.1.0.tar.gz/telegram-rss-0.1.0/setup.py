# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_rss', 'telegram_rss.commands']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'bleach>=3.2.3,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'feedparser>=6.0.2,<7.0.0',
 'python-telegram-bot>=13.1,<14.0',
 'requests>=2.25.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['telegram-rss = telegram_rss.main:main']}

setup_kwargs = {
    'name': 'telegram-rss',
    'version': '0.1.0',
    'description': 'Fetch rss and send the latest update to telegram.',
    'long_description': None,
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
