# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['us_pls',
 'us_pls._download',
 'us_pls._logger',
 'us_pls._persistence',
 'us_pls._scraper',
 'us_pls._stats',
 'us_pls._transformer',
 'us_pls._variables',
 'us_pls._variables.fy2018']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'pandas>=1.2.1,<2.0.0',
 'punq>=0.4.1,<0.5.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'us-pls',
    'version': '0.0.2a7',
    'description': 'Client to get and analyze data from the US Public Library Survey',
    'long_description': '# us-pls\n\nA client to pull and query data from the Public Libraries Survey.\n\n<!--ts-->\n   * [us-pls](#us-pls)\n      * [The Public Libraries Survey](#the-public-libraries-survey)\n      * [Installation](#installation)\n      * [Getting started](#getting-started)\n      * [Getting data](#getting-data)\n      * [Understanding the variables](#understanding-the-variables)\n         * ["But I don\'t want to read!"](#but-i-dont-want-to-read)\n\n<!-- Added by: runner, at: Sun Jan 31 19:32:11 UTC 2021 -->\n\n<!--te-->\n\n## The Public Libraries Survey\n\nFrom the Institute of Museum and Library Services\' [website](https://www.imls.gov/research-evaluation/data-collection/public-libraries-survey):\n\nThe Public Libraries Survey (PLS) examines when, where, and how library services are changing to meet the needs of the public. These data, supplied annually by public libraries across the country, provide information that policymakers and practitioners can use to make informed decisions about the support and strategic management of libraries.\n\n## Installation\n\n```bash\npip install us-pls\n```\n\n## Getting started\n\nBegin by selecting the year of the survey:\n\n```python\n>>> from us_pls import PublicLibrariesSurvey\n>>> pls_client = PublicLibrariesSurvey(year=2017)\n\n<PublicLibrariesSurvey 2017>\n```\n\n## Getting data\n\nThe survey offers three datasets:\n\n1. Public Library System Data File (`DatafileType.SystemData`). This contains one row per library in the US\n2. Public Library State Summary/State Characteristics Data File (`DatafileType.StateSummaryAndCharacteristicData`). The contains one row per state in the US, as well as outlying areas.\n3. Public Library Outlet Data File (`OutletData`). The contains data for public library service outlets (e.g., central, branch, bookmobile, and books-by-mail-only outlets)\n\nTo select and query a dataset, do the following:\n\n```python\n>>> from us_pls import DatafileType\n>>> pls_client.get_stats(_for=DatafileType.<Type of interest>)\n\n<pandas.DataFrame with the data>\n```\n\n## Understanding the variables\n\nUnfortunately, the PLS does not have any API serving its data. As a result, this client works by scraping the PLS page (which contains all of its surveys), storing its survey and documentation URLs, and then downloading the surveys and documentation for the year of interest.\n\nBecause the documentation files are PDFs, and lack a standardized formatting from year to year, there is no deterministic way to extract variable data from them programmatically.\n\nAs a result, the client will also download a given year\'s survey\'s documentation. (By default it will store this in the your current directory under `data/<survey-year>/Documentation.pdf`.) So, if you want to verify what a variable name means, or, if you\'d like to read more about that survey\'s methodology, that documentation file will be your friend.\n\n### "But I don\'t want to read!"\n\nIf you really hate reading, or you want a broad overview of what each datafile contains, run the following (we\'re using the Outlet Data file as an example):\n\n```python\n>>> pls_client.read_docs(on=DatafileType.OutletData)\n\n"Public Library Outlet Data File includes..."\n```\n',
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
