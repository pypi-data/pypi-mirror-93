# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['journal_crawler', 'journal_crawler.journals']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'requests>=2.25.1,<3.0.0',
 'ythesis>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'journal-crawler',
    'version': '0.0.1',
    'description': 'provides thesis entities',
    'long_description': 'journal crawler\n================================================================================\n',
    'author': 'yassu',
    'author_email': 'yasu0320.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/yassu/ythesis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
