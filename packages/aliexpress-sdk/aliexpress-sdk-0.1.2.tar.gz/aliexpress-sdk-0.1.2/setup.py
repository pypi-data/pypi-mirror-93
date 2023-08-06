# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aliexpress',
 'aliexpress.api',
 'aliexpress.api.rest',
 'aliexpress.api.rest.logistics',
 'aliexpress.scripts']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.4,<4.0.0']

entry_points = \
{'console_scripts': ['aliexpress-cli = aliexpress.scripts.cli:main']}

setup_kwargs = {
    'name': 'aliexpress-sdk',
    'version': '0.1.2',
    'description': 'Python wrapper of the AliExpress API for sellers',
    'long_description': '# AliExpress Seller API SDK\n\nPython wrapper of the AliExpress API for sellers.\nSee the original API documentation at the [Ali Express Open Platform](https://developers.aliexpress.com/en/doc.htm) web site.\n\n[![Python](https://img.shields.io/badge/Python-3.x-%23FFD140)](https://www.python.org/)\n[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://choosealicense.com/licenses/mit/)\n[![GitHub last commit](https://img.shields.io/github/last-commit/bayborodin/aliexpress-sdk)](https://github.com/bayborodin/aliexpress-sdk)\n\n## How to install\n```\npip install aliexpress-sdk\n```\nor (for pre-release):\n```sh\npip install git+https://github.com/bayborodin/aliexpress-sdk\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nBefore sending a pull request, please make sure that all tests pass and that the linter has no comments on your code.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Nicholas Bayborodin',
    'author_email': 'nicholas.bayborodin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bayborodin/aliexpress-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
