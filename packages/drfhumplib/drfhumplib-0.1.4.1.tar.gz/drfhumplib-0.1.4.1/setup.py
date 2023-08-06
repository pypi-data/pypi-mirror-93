# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drfhumplib']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.5.4,<4.0.0', 'humplib==0.1.1']

setup_kwargs = {
    'name': 'drfhumplib',
    'version': '0.1.4.1',
    'description': 'a drf hump to underline tool',
    'long_description': None,
    'author': 'huoyinghui',
    'author_email': 'yhhuo@yunjinginc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydtools/drfhumplib/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
