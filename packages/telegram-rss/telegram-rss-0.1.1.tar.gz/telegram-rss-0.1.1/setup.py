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
    'version': '0.1.1',
    'description': 'Fetch rss and send the latest update to telegram.',
    'long_description': '# Telegram RSS\n\n[![PyPi Package Version](https://img.shields.io/pypi/v/telegram-rss)](https://pypi.org/project/telegram-rss/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/telegram-rss)](https://pypi.org/project/telegram-rss/)\n[![LICENSE](https://img.shields.io/github/license/pentatester/telegram-rss)](https://github.com/pentatester/telegram-rss/blob/master/LICENSE)\n[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)\n\nFetch rss and send the latest update to telegram.\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pentatester/telegram-rss',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
