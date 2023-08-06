# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['excel_ngrams']

package_data = \
{'': ['*']}

install_requires = \
['XlsxWriter>=1.3.7,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'nltk>=3.5,<4.0',
 'openpyxl>=3.0.6,<4.0.0',
 'pandas>=1.2.1,<2.0.0',
 'spacy>=2.3.5,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.4.0,<4.0.0']}

entry_points = \
{'console_scripts': ['excel-ngrams = excel_ngrams.console:main']}

setup_kwargs = {
    'name': 'excel-ngrams',
    'version': '0.1.1',
    'description': 'An app to output n-grams from column in Excel spreadsheet',
    'long_description': None,
    'author': 'Matthew Oliver',
    'author_email': 'matthewoliver@live.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mattyocode/excel-ngrams',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
