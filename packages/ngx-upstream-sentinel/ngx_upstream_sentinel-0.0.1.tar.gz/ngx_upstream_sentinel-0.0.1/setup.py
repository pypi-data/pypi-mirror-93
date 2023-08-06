# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ngx_upstream_sentinel',
 'ngx_upstream_sentinel.ngx_upstream_sentinel',
 'ngx_upstream_sentinel.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ngx-upstream-sentinel',
    'version': '0.0.1',
    'description': 'Smart Sentinel for Upstreams to nginx',
    'long_description': None,
    'author': 'Rodrigo Pinheiro Matias',
    'author_email': 'rodrigopmatias@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
