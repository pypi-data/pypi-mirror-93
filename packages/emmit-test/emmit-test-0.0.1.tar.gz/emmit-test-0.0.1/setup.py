# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['namespace_test']

package_data = \
{'': ['*']}

extras_require = \
{'dns': ['dnspython==1.16'], 'pandas': ['pandas==1.0.5']}

setup_kwargs = {
    'name': 'emmit-test',
    'version': '0.0.1',
    'description': 'test',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
}


setup(**setup_kwargs)
