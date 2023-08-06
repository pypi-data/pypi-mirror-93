# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faust_prometheus_monitor']

package_data = \
{'': ['*']}

install_requires = \
['faust-streaming>=0.4.6,<0.5.0', 'prometheus-client>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'faust-prometheus-monitor',
    'version': '0.1.6',
    'description': 'prometheus monitor for faust',
    'long_description': None,
    'author': 'Hamzah Qudsi',
    'author_email': 'hamzah.qudsi@kensho.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
