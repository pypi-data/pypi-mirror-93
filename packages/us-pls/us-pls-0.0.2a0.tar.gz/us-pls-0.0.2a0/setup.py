# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['us_pls',
 'us_pls._download',
 'us_pls._logger',
 'us_pls._scraper',
 'us_pls._stats']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'pandas>=1.2.1,<2.0.0',
 'punq>=0.4.1,<0.5.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'us-pls',
    'version': '0.0.2a0',
    'description': 'Client to get and analyze data from the US Public Library Survey',
    'long_description': '# us-libraries\n\n<!--ts-->\n<!--te-->\n',
    'author': 'Joel Krim',
    'author_email': 'drawjk705@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drawjk705/us-libraries',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
