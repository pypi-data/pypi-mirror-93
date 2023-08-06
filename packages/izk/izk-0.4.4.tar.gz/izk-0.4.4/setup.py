# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['izk']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.4,<3.0.0',
 'colored>=1.4.2,<2.0.0',
 'kazoo>=2.8.0,<3.0.0',
 'prompt-toolkit>=3.0.14,<4.0.0']

entry_points = \
{'console_scripts': ['izk = izk.prompt:main']}

setup_kwargs = {
    'name': 'izk',
    'version': '0.4.4',
    'description': 'Zookeeper CLI with autocomplete, syntax highlighting and pretty printing',
    'long_description': None,
    'author': 'Balthazar Rouberol',
    'author_email': 'br@imap.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
