# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uquake', 'uquake.core', 'uquake.core.util', 'uquake.waveform']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.19.0,<8.0.0',
 'jedi==0.17.2',
 'loguru>=0.5.3,<0.6.0',
 'numpy==1.18.0',
 'obspy>=1.2.2,<2.0.0',
 'openpyxl>=3.0.6,<4.0.0',
 'pandas>=1.2.1,<2.0.0',
 'pytest>=6.2.1,<7.0.0',
 'setuptools>=51.3.3,<52.0.0']

setup_kwargs = {
    'name': 'uquake',
    'version': '0.1.0',
    'description': 'extension of the ObsPy library for local seismicity',
    'long_description': None,
    'author': 'uQuake development team',
    'author_email': 'dev@uQuake.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
